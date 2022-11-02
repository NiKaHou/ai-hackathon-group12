from socket import SocketIO
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import faiss
from imp import load_module
from transformers import BertTokenizer, TFBertForSequenceClassification, glue_convert_examples_to_features
import pandas as pd
import tensorflow as tf
import numpy as np
import os
import tensorflow as tf
import tensorflow_datasets as tfds
from sklearn.metrics import classification_report, confusion_matrix
import torch
from sentence_transformers import SentenceTransformer
from functools import reduce
import json

app = Flask(__name__)
CORS(app)
ngpus = faiss.get_num_gpus()
print("number of GPUs:", ngpus)
os.chdir('C:/hack/17666-front/ai-hackathon-group12/17666-flask')
questionData = pd.read_csv('C:/hack/17666-front/ai-hackathon-group12/17666-flask/test_question.csv')
model = SentenceTransformer('peterchou/simbert-chinese-base')
# Check if GPU is available and use it
if torch.cuda.is_available():
    model = model.to(torch.device("cuda"))
print(model.device)

# Convert question to vectors
embeddings = model.encode(questionData.question.to_list(), show_progress_bar=True)

# Step 1: Change data type
embeddings = np.array([embedding for embedding in embeddings]).astype("float32")

# Step 2: Instantiate the index
index = faiss.IndexFlatL2(embeddings.shape[1])

# Step 3: Pass the index to IndexIDMap
index = faiss.IndexIDMap(index)

# Step 4: Add vectors and their IDs
index.add_with_ids(embeddings, questionData.id.values)

print(f"Number of vectors in the Faiss index: {index.ntotal}")

faiss.write_index(index,"{}.index".format('faiss_index'))


class predict3Class:
    idx = ""
    likely = 0

    def __init__(self,x_idx,y_likely):
        self.idx = x_idx
        self.likely = y_likely

# tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
# new_model = TFBertForSequenceClassification.from_pretrained("C:/hack/17666-front/ai-hackathon-group12/17666-flask/")

@app.route('/')
def aaa():
    return 'hello man'

@app.route('/predict')
def predict():
        
        sentence1 = ["客戶指定貨代付款要提供什麼？"] #User input
        sentence2 = ["付款的不是客戶"] # 400

        test_dataset = pd.DataFrame(dict(idx=list(range(len(sentence1))),
                                 label=[0]*len(sentence1),
                                 sentence1=sentence1,
                                 sentence2=sentence2))
        max_length= 128
        task = 'mrpc'
        test_gen = tf.data.Dataset.from_tensor_slices(dict(test_dataset))
        test_gen = glue_convert_examples_to_features(test_gen, tokenizer, max_length, task)
        test_gen = test_gen.batch(1)
        next(iter(test_gen))

        #---------------------------------------------
        pred = new_model.predict(test_gen)
        print(pred)
        pred_ids = np.argmax(pred[0], axis=-1)
        if (pred_ids[0] == 1):
            return sentence2[0]
        else:
            return "different"



@app.route("/predict2")
def predict2():
    query = [" ".join( [ word for word in '詢證函要找誰處理?' ])]
    print("bert-serving input: ",query)
    vectors = model.encode(query)
    #vectors = normaliz_vec(vectors.tolist())
    vecList=vectors.tolist()

    for i in range(len(vecList)):
            vec = vecList[i]
            square_sum = reduce(lambda x, y: x+y, map(lambda x: x*x, vec))
            sqrt_square_sum = np.sqrt(square_sum)
            coef = 1/sqrt_square_sum
            vec = list(map(lambda x: x*coef, vec))
            vecList[i] = vec



    query_list = np.array(vectors).astype('float32')
    dis,ind = index.search( query_list,k=5 )
    print(type(ind[0][0]))
    return (str(ind[0][0]))

def obj_dict(obj):
    return obj.__dict__

@app.route("/predict3", methods=['POST'])
def predict3():
    request_data = request.get_json()
    print(request_data)
    query = [" ".join( [ word for word in request_data['question'] ])]
    print("bert-serving input: ",query)
    vectors = model.encode(query)
    #vectors = normaliz_vec(vectors.tolist())
    vecList=vectors.tolist()

    for i in range(len(vecList)):
            vec = vecList[i]
            square_sum = reduce(lambda x, y: x+y, map(lambda x: x*x, vec))
            sqrt_square_sum = np.sqrt(square_sum)
            coef = 1/sqrt_square_sum
            vec = list(map(lambda x: x*coef, vec))
            vecList[i] = vec

    

    query_list = np.array(vectors).astype('float32')
    dis,ind = index.search( query_list,k=5 )
    response = []
    top_number=1
    for id in ind[0]:
        print("*top {}".format(top_number))
        print("距離差異: {}".format(np.format_float_positional(np.float32(dis[0][top_number-1]))))
        print("id: {}".format(id))
        response.append(predict3Class(str(id),np.format_float_positional(np.float32(dis[0][top_number-1]))))

        top_number =top_number+1
    
    print(response)
    response_json = json.dumps(response,default=obj_dict)
    return (json.dumps(response_json))



if __name__ == '__main__':
    app.debug = True
    app.run()


    