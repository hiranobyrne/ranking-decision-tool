import os


class Config:
    # root_path = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = os.getenv("SECRET_KEY", "passe_modificar")

    DEBUG = True
    # DEBUG = os.getenv("FLASK_DEBUG", False)

    SESSION_TYPE = os.getenv("SESSION_TYPE", "filesystem")
    SESSION_PERMANENT = os.getenv("SESSION_PERMANENT", False)
    # app.config['SESSION_PERMANENT'] = False

    # DATA_FILE = os.path.join("data", "cars.csv")
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
    MODELS_DIR = os.path.join(os.path.dirname(__file__), '../data/ml_models/')

    SVM_ZIP_PATH = os.path.join(MODELS_DIR, 'svm_model.zip')
    SVM_MODEL_PATH = os.path.join(MODELS_DIR, 'svm_model.pkl')
    KNN_ZIP_PATH = os.path.join(MODELS_DIR, 'knn_model.zip')
    KNN_MODEL_PATH = os.path.join(MODELS_DIR, 'knn_model.pkl')
    SCALER_PATH = os.path.join(MODELS_DIR, 'scaler.pkl')

# codigo de './frontend'
# def __init__(self, root_path):
#     self.MODELS_DIR = os.path.join(root_path, 'models')
#     self.SVM_ZIP_PATH = os.path.join(self.MODELS_DIR, 'svm_model.zip')
#     self.SVM_MODEL_PATH = os.path.join(self.MODELS_DIR, 'svm_model.pkl')
#     self.KNN_ZIP_PATH = os.path.join(self.MODELS_DIR, 'knn_model.zip')
#     self.KNN_MODEL_PATH = os.path.join(self.MODELS_DIR, 'knn_model.pkl')
#     self.SCALER_PATH = os.path.join(self.MODELS_DIR, 'scaler.pkl')
