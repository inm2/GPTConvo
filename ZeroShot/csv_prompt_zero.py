import openai
import pandas as pd
import streamlit as st
import sys
from io import StringIO
import matplotlib
import re
matplotlib.use('tkagg')

# The purpose of this file is to handle CSV files -> convert to a dataframe
# and enable a conversation from the dataframe
# The next step after is to return the response and execute it in streamlit

# Tokens
def token_amount(completion):
   total_tokens = completion.usage.total_tokens
   prompt_tokens = completion.usage.prompt_tokens
   completion_tokens = completion.usage.completion_tokens
   return total_tokens, prompt_tokens, completion_tokens

def reset_everything():
   st.session_state['messages'] = [{"role": "assistant", "content": "How can I help you today?"}]
   

def csv_reader(file_name):

    df = pd.read_csv(file_name)
    num_rows, num_col = len(df.index), len(df.columns)
    df_head = df.head()
    
    csv_content = f"""You are provided with a Pandas dataframe {df} with {num_rows} and {num_col}.
        The metadata of the dataframe is: {df_head}. 
        When asked about the data, the response given should include the python code that describes the dataframe 'df'.
        Using the provided dataframe, df, return the Python code to get the answer to the following question: """
    
    # if selection == 'One-Shot':
    messages = [{"role": "system", "content": csv_content},]
       
#     if selection == 'Few-Shot':
#         example_text = """import matplotlib.pyplot as plt
# top_5_happiest_countries = df.sort_values('happiness_index', ascending=False).head(5)
# plt.bar(top_5_happiest_countries['country'], top_5_happiest_countries['happiness_index'], color=['blue', 'green', 'yellow', 'red', 'purple'])
# plt.xlabel('Country') plt.ylabel('Happiness Index') plt.title('Top 5 Happiest Countries')
# plt.show()"""

#         messages = [{"role": "system", "content": csv_content},
#                     {"role": "user", "content": "Give me the Top 5 happiest countries in a plot with different colors."},
#                     {"role": "assistant", "content": example_text},]
    
    # Initalize session state variable
    if 'messages' not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you today?"}]
        
    # Write to the Streamlit chat
    for msg in st.session_state.messages:
      st.chat_message(msg["role"]).write(msg["content"])
      
    # Get user input and OpenAI output
    if prompt := st.chat_input():
      # Prompt the user input
      st.session_state.messages.append({"role": "user", "content": prompt})
      st.chat_message("user").write(prompt)
      print(st.session_state.messages)
      print("Messages: ", messages)

      # Append all of the messages to pass into OpenAI Model
      messages += st.session_state["messages"]

      response = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
                                              messages=messages,
                                              temperature=0,
                                              max_tokens = 1024)

      msg = response.choices[0].message

      st.session_state.messages.append(msg)

      print("MSG: \n\n", msg)
      print("Session State: \n\n", st.session_state.messages)

      # Get the return from OpenAI
      st.chat_message("assistant").write(msg.content)

      total_tokens, prompt_tokens, completion_tokens = token_amount(completion=response)
      
      cost = ((prompt_tokens * .0015) + (completion_tokens * .002)) / 1000

      st.write(f'Total Tokens: {total_tokens}')
      st.write(f'Embedding (Input) Cost in USD: {cost}')

      # Execute code
      
        # Extract the code content using regular expression
      code_content = re.search(r'```python\n(.*?)\n```', msg['content'], re.DOTALL)

      if code_content:
        code_snippet = code_content.group(1)
        print(code_snippet)
        exec(code_snippet)
      else:
        print("No code snippet found.")
      

      #print(messages)

