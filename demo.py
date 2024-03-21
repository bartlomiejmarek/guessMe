import argparse
import random
import time

import gradio as gr

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name',type=str,default='gpt3')
    parser.add_argument('--mode',type=str,default='easy')
    parser.add_argument('--n',type=int,default='20')

    with gr.Blocks() as demo:
        chatbot = gr.Chatbot()
        msg = gr.Textbox()
        clear = gr.Button("清除")

        def respond(message, chat_history):
            bot_message = random.choice(["你好吗？", "我爱你", "我很饿"])
            chat_history.append((message, bot_message))
            time.sleep(1)
            return "", chat_history

        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        clear.click(lambda: None, None, chatbot, queue=False)

    demo.launch()