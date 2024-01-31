from keras.models import Model,Sequential
from keras.layers import Input, Embedding, LSTM, SimpleRNN, concatenate, Dense, Dropout
from src.constant.constants import PARAMS_FILE

class ModelFactory:
    def __init__(self):
        self.__params = PARAMS_FILE['model_params']
        self.__data_processing_params = self.__params['data_processing']
        self.__model_training_params = self.__params['model_training']

        self.__max_words = self.__data_processing_params['max_words']
        self.__max_sequence_length = self.__data_processing_params['max_sequence_length']
        self.__optimizer = self.__model_training_params['optimizer']
        self.__loss = self.__model_training_params['loss']
        self.__dropout = self.__model_training_params['dropout']
        self.__embedding_dim = self.__model_training_params['embedding_dim']
        self.__nurons_unit = self.__model_training_params['nurons_unit']
        self.__hidden_activation = self.__model_training_params['hidden_activation']
        self.__out_put_activation = self.__model_training_params['out_put_activation']

    def build_rnn_model(self):
        ## we can apply fuctional approach as well
        model = Sequential()
        model.add(Embedding(input_dim=self.__max_words, output_dim=self.__embedding_dim, input_length=self.__max_sequence_length ))
        model.add(SimpleRNN(self.__nurons_unit,dropout=self.__dropout,recurrent_dropout=self.__dropout))
        model.add(Dense(1, activation=self.__out_put_activation))
        model.compile(optimizer=self.__optimizer, loss=self.__loss, metrics=['accuracy'])
        return model

    def build_lstm_model(self):
        model = Sequential()
        model.add(Embedding(input_dim=self.__max_words, output_dim=self.__embedding_dim, input_length=self.__max_sequence_length))
        model.add(LSTM(self.__nurons_unit,dropout=self.__dropout,recurrent_dropout=self.__dropout))
        model.add(Dense(1, activation=self.__out_put_activation))
        model.compile(optimizer=self.__optimizer, loss=self.__loss, metrics=['accuracy'])
        return model

    def build_combined_model(self):
        ## we have explore more
        input_layer = Input(shape=(self.__max_sequence_length,))
        embedding_layer = Embedding(input_dim=self.__max_words, output_dim=self.__embedding_dim)(input_layer)

        lstm_branch = LSTM(self.__nurons_unit)(embedding_layer)
        rnn_branch = SimpleRNN(self.__nurons_unit)(embedding_layer)

        combined_layer = concatenate([lstm_branch, rnn_branch])

        x = Dense(self.__nurons_unit, activation=self.__hidden_activation)(combined_layer)
        x = Dropout(self.__dropout)(x)
        output_layer = Dense(1, activation=self.__out_put_activation)(x)

        model = Model(inputs=input_layer, outputs=output_layer)
        model.compile(optimizer=self.__optimizer, loss=self.__loss, metrics=['accuracy'])
        return model
    
    def build_model_type(self, model_type):
        if model_type == 'rnn':
            return self.build_rnn_model()
        elif model_type == 'lstm':
            return self.build_lstm_model()
        elif model_type == 'combined':
            return self.build_combined_model()
        else:
            raise ValueError(f"Invalid model_type: {model_type}. Supported types are 'rnn', 'lstm', and 'combined'.")