import os
from application import app

if __name__ == '__main__':
    app.run(debug = True)

# if __name__=="__main__":
#     app.run(host=os.getenv('IP', '0.0.0.0'), 
#             port=int(os.getenv('PORT', 5000)))