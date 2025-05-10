import streamlit as st
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_aws import ChatBedrockConverse
from langgraph.prebuilt import create_react_agent
import json

st.set_page_config(
    page_title="テストアプリ",
    layout="wide"
)

st.title("テストアプリ")
st.markdown("お話ししましょう！")

# Initialize session state for storing conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("質問を入力してください")

# Function to extract thinking process and final answer from messages
def extract_messages(response):
    thinking_process = []
    final_answer = ""
    
    if "messages" in response:
        messages = response["messages"]
        
        # Extract thinking process (all messages except the last AIMessage)
        for msg in messages:
            # Check if it's a message with content
            if hasattr(msg, "__class__"):
                msg_type = msg.__class__.__name__
                # Convert technical message type to user-friendly label
                friendly_label = "メッセージ"
                if msg_type == "HumanMessage":
                    friendly_label = "あなたの入力"
                elif msg_type == "AIMessage":
                    friendly_label = "エージェントの回答"
                elif msg_type == "ToolMessage":
                    friendly_label = "ツールの実行結果"
                elif msg_type == "SystemMessage":
                    friendly_label = "システムメッセージ"
                
                if hasattr(msg, "content"):
                    content = msg.content
                    
                    # Handle different content formats
                    if isinstance(content, list):
                        # If content is a list of components, extract text parts
                        text_parts = []
                        for item in content:
                            if isinstance(item, dict) and item.get("type") == "text":
                                text_parts.append(item.get("text", ""))
                        content = " ".join(text_parts)
                    
                    # Add to thinking process with user-friendly label
                    if content:
                        thinking_process.append(f"**{friendly_label}**: {content}")
        
        # Get the last AIMessage as the final answer
        for msg in reversed(messages):
            if hasattr(msg, "__class__") and msg.__class__.__name__ == "AIMessage":
                if hasattr(msg, "content"):
                    content = msg.content
                    if isinstance(content, list):
                        text_parts = []
                        for item in content:
                            if isinstance(item, dict) and item.get("type") == "text":
                                text_parts.append(item.get("text", ""))
                        content = " ".join(text_parts)
                    final_answer = content
                    break
    
    return thinking_process, final_answer

# Function to process user input and get agent response
async def process_input(user_input):
    # Create a placeholder for displaying tool execution status
    status_container = st.empty()
    status_container.info("考え中... 🤔")
    
    # Use the model from session state
    model = ChatBedrockConverse(
        model=st.session_state.model_id
    )
    
    try:
        # Use the MCP server URL from session state
        async with MultiServerMCPClient(
            {
                "weather": {
                    "url": st.session_state.mcp_server_url,
                    "transport": "sse",
                }
            }
        ) as client:
            # Create the agent with tools
            agent = create_react_agent(model, client.get_tools())
            
            # Update status
            status_container.info("ツールを準備しました 🛠️")
            
            # Invoke the agent with user input
            status_container.info("質問を処理中... ⚙️")
            
            # Simple invocation without callbacks
            response = await agent.ainvoke({"messages": user_input})
            
            # Clear the status and return the response
            status_container.empty()
            return response
            
    except Exception as e:
        status_container.error(f"エラーが発生しました: {str(e)}")
        return {"output": f"エラーが発生しました: {str(e)}"}

# Process user input when provided
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Display assistant response
    with st.chat_message("assistant"):
        response_container = st.empty()
        response_container.info("考え中... 🤔")
        
        # Process the input asynchronously
        response = asyncio.run(process_input(user_input))
        
        try:
            # Extract thinking process and final answer
            thinking_process, final_answer = extract_messages(response)
            
            # Create a container for the formatted response
            formatted_response = st.container()
            
            with formatted_response:
                # Display thinking process in an expander/accordion
                if thinking_process:
                    with st.expander("エージェントの思考過程 🧠"):
                        for thought in thinking_process:
                            st.markdown(thought)
                
                # Display final answer
                if final_answer:
                    st.markdown(f"### エージェントの回答\n\n{final_answer}")
                else:
                    st.markdown("### エージェントの回答\n\n回答に失敗しました...")
            
            # Prepare a text version for the chat history
            if final_answer:
                assistant_response = f"エージェントの回答\n\n{final_answer}"
            else:
                assistant_response = "エージェントの回答\n\n回答に失敗しました..."
            
            # Clear the loading message
            response_container.empty()
            
        except Exception as e:
            assistant_response = f"回答の処理中にエラーが発生しました\n\n{str(e)}\n\n生のレスポンス: {str(response)}"
            response_container.markdown(assistant_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

# Add a sidebar with information and configuration
with st.sidebar:
    # Configuration section
    st.header("設定 ⚙️")
    
    # Initialize session state for configuration
    if "mcp_server_url" not in st.session_state:
        st.session_state.mcp_server_url = "http://ECSのIP:8000/sse"
    
    if "model_id" not in st.session_state:
        st.session_state.model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    
    # MCP server URL configuration
    st.text_input(
        "MCP サーバーURL", 
        value=st.session_state.mcp_server_url,
        key="mcp_server_url"
    )
    
    # Model selection
    st.selectbox(
        "使用するモデル",
        [
            "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            "us.anthropic.claude-3-5-sonnet-20240620-v1:0",
            "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
            "us.anthropic.claude-3-5-haiku-20241022-v1:0"
        ],
        index=0,
        key="model_id"
    )
    
    # Add a clear chat button
    if st.button("会話履歴をクリア"):
        st.session_state.messages = []
        st.rerun()