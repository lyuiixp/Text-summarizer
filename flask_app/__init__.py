from flask import Flask, render_template, request, redirect, url_for
import re
from transformers import PreTrainedTokenizerFast
import torch
import joblib

def create_app():
    app = Flask(__name__)

    @app.route('/')  ## => 127.0.0.1:5000/
    def index():
        return render_template('index.html')
    
    @app.route('/summarize', methods=["POST"])
    def summarize():
        if request.method=="POST":
            result = request.form['input_text']

            text_dir = 'C:\\Users\\Yong\\코드스테이츠 AI\\Section Project\\Project1\\text\\'
            stopwords = open(text_dir+'stopwords.txt', mode='rt', encoding='utf-8')
            stop_words = stopwords.read().split('\n')

            def preprocess_sentence(sentence, remove_stopwords =True):
                sentence = re.sub('([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', '', sentence) # email주소 제거
                sentence = re.sub('(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', '', sentence) # url 제거
                sentence = re.sub('([ㄱ-ㅎㅏ-ㅣ]+)', '', sentence)  # 한글자음, 모음 제거 (ㅋㅋㅎㅎ..)
                sentence = re.sub('<[^>]*>', '', sentence)          # html태그 제거(<H1> .. </H1>)
                sentence = re.sub('[-=+#/\?:^$@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\…》]', '', sentence)
                
                if remove_stopwords:    # text
                    tokens = ' '.join(word for word in sentence.split() if not word in stop_words if len(word)>1)
                else:                   # abstract
                    tokens = ' '.join(word for word in sentence.split() if len(word)>1)
                return tokens

            model_test = joblib.load('C:/Users/Yong/코드스테이츠 AI/Section Project/Project1/flask_app/model/model.pkl')

            news_text = preprocess_sentence(result)
            tokenizer = PreTrainedTokenizerFast.from_pretrained("gogamza/kobart-summarization")
            input_ids = tokenizer.encode(news_text)
            input_ids = [tokenizer.bos_token_id] + input_ids + [tokenizer.eos_token_id]
            input_ids = torch.tensor([input_ids])

            model_summary = model_test.generate(
                input_ids=input_ids,
                bos_token_id=model_test.config.bos_token_id,
                eos_token_id=model_test.config.eos_token_id,
                length_penalty=2.0, # 길이에 대한 penalty값. 1보다 작은 경우 더 짧은 문장을 생성하도록 유도하며, 1보다 클 경우 길이가 더 긴 문장을 유도
                max_length=128,     # 요약문의 최대 길이 설정
                min_length=32,      # 요약문의 최소 길이 설정
                num_beams=4,        # 문장 생성시 다음 단어를 탐색하는 영역의 개수 
            )
            sum_text= tokenizer.decode(model_summary.squeeze(), skip_special_tokens=True)
            return render_template('index.html', sum_text=sum_text)

    return app

#if __name__ =='__main__':
#    app.run(debug=True)
