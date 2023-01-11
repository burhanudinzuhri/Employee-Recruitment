from tensorflow import keras
import numpy as np
import pickle
import warnings
warnings.filterwarnings("ignore")

# global variable
global model, scaler

def predict_prob(number):
    return [number[0],1-number[0]]

# load model and scaler
def load():
    global model, scaler
    model = keras.models.load_model('model/model_ds.h5')
    scaler = pickle.load(open('model/scaler_ds.pkl', 'rb'))

# function data prediction and result return
def predict_data(data):
    if (data[0] == 'No'):
        doj_extended_pred = 0
    else:
        doj_extended_pred = 1
    if (data[3] == 'E0'):
        offered_band_pred = 0
    elif (data[3] == 'E1'):
        offered_band_pred = 1
    elif (data[3] == 'E2'):
        offered_band_pred = 2
    else:
        offered_band_pred = 3
    if (data[7] == 'No'):
        joining_bonus_pred = 0
    else:
        joining_bonus_pred = 1
    if (data[8] == 'No'):
        candidate_relocate_actual_pred = 0
    else:
        candidate_relocate_actual_pred = 1
    if (data[9] == 'Female'):
        gender_pred = 0
    else:
        gender_pred = 1
    if (data[10] == 'Agency'):
        candidate_source_pred = 0
    elif (data[10] == 'Direct'):
        candidate_source_pred = 1
    else:
        candidate_source_pred = 2
    if (data[12] == 'AXON'):
        lob_pred = 0
    elif (data[12] == 'BFSI'):
        lob_pred = 1
    elif (data[12] == 'CSMP'):
        lob_pred = 2
    elif (data[12] == 'EAS'):
        lob_pred = 3
    elif (data[12] == 'ERS'):
        lob_pred = 4
    elif (data[12] == 'ETS'):
        lob_pred = 5
    elif (data[12] == 'Healthcare'):
        lob_pred = 6
    elif (data[12] == 'INFRA'):
        lob_pred = 7
    else:
        location_pred = 8
    if (data[13] == 'Ahmedabad'):
        location_pred = 0
    elif (data[13] == 'Bangalore'):
        location_pred = 1
    elif (data[13] == 'Chennai'):
        location_pred = 2
    elif (data[13] == 'Cochin'):
        location_pred = 3
    elif (data[13] == 'Gurgaon'):
        location_pred = 4
    elif (data[13] == 'Hyderabad'):
        location_pred = 5
    elif (data[13] == 'Kolkata'):
        location_pred = 6
    elif (data[13] == 'Mumbai'):
        location_pred = 7
    elif (data[13] == 'Noida'):
        location_pred = 8
    elif (data[13] == 'Pune'):
        location_pred = 9
    else:
        location_pred = 10
    duration_to_accept_the_offer_pred = data[1]
    notice_period_pred = data[2]
    percent_hike_expected_in_ctc_pred = data[4]
    percent_hike_offered_in_ctc_pred = data[5]
    percent_difference_ctc_pred = data[6]
    rex_in_yrs_pred = data[11]
    age_pred = data[14]
    
    # input data into an array
    data_fix = [[doj_extended_pred, duration_to_accept_the_offer_pred, notice_period_pred, offered_band_pred, percent_hike_expected_in_ctc_pred, percent_hike_offered_in_ctc_pred, percent_difference_ctc_pred, joining_bonus_pred, candidate_relocate_actual_pred, gender_pred, candidate_source_pred, rex_in_yrs_pred, lob_pred, location_pred, age_pred]]
    
    # data prediction
    data_fix = scaler.transform(data_fix)
    prediksi = model.predict(data_fix)
    
    # probability
    probability = np.array(list(map(predict_prob, prediksi)))[0]
    probability = max(probability) * 100
    probability = round(probability,2)
    
    if probability >= 0 and probability < 0.5:
        predict_result = "Not Joined"
    else:
        predict_result = "Joined"

    opt = keras.optimizers.Adam(lr=0.0001)
    model.compile(optimizer=opt, loss='binary_crossentropy')
    model.fit(data_fix, prediksi, epochs = 60, batch_size = 200, verbose=0)
    model.save('model/model_ds.h5')
    
    return [predict_result, probability]


