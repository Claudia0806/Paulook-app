
#APIS
import uvicorn
from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel
from typing import Union

app = FastAPI()
# definimos una  lase para las variables del primer endpoint
# Una clase para definir
class Posts(BaseModel):
    n_likes: int
    description: str
    user_id: int
    creation_date: Union[datetime,None]= None# hacemos opcional agregarlo
    post_id: str
    title_post : str

class Users(BaseModel):
    user_name: str
    user_id: int
    user_age: int
    user_rol: str
    rol_id: int
    # los siguientes son opcionales
    career: Union[str,None]=None
    semester:Union[str,None]=None
    friend_list: list[int]

posts_dict = {}
users_dict = {}

#Primer endpoint es una función body
@app.put('/posts')
def CreatePost (post: Posts):
    # como estamos llamando una clase arriba tenemos que volverlo diccionario para que sea un diccionario de diccionarios
    post = post.dict()
    posts_dict [post['post_id']] = post

    # se regresa en diccionario por que esa es la estructura
    return {'Description':f'Post creado correctamente {post["post_id"]}'}


#Segundo endpoint es una función body
@app.put('/users')
def CreateUser (user: Users):
    user = user.dict()
    users_dict [user['user_id']] = user

    # se regresa en diccionario por que esa es la estructura
    return {'Description':f'Usuario creado correctamente {user["user_id"]}'}

#Tercer endpoint es una función body
@app.post('/users/{user_id}/{friend_id}')
def UpdateUser(user_id : int ,friend_id: int):
    # en el diccionario de usuarios buscamos el user_id
    user_to_update = users_dict[user_id]
    # se crea una lista que guarde al amigo
    list_to_update = user_to_update["friend_list"]
    # se agrega a la lista el usuario
    list_to_update.append(friend_id)
    # se agrega a un diccionario
    users_dict[user_id]['friend_list'] = list_to_update
    return {'Description':f'Agregamos {users_dict[user_id]} correctamente'}

# Cuarto endpoint
@app.get('/users/{user_id}/friends')
def GetFriendList(user_id :int):
    get_friends = users_dict[user_id]["friend_list"]
    return {'User ID': user_id, 'Friend_list': get_friends}




# Esta funcion es necesaria siempre
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", reload=True)
