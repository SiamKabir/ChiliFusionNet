from .main_model import load_joblib, load_json
# from .preprocess import get_test_features
from .single_preprocess import get_single_test_feature
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pickle")




# def predict_df_dengue(df: pd.DataFrame):
#     """
#     Predict dengue status for a batch of input data (as DataFrame).
#     Returns a list of (prediction, probability) tuples.
#     """
#     X = preprocess_df_input(df)
    
#     # Predict labels and probabilities
#     predictions = stack_model.predict(X)
#     probabilities = stack_model.predict_proba(X)[:, 1]  # Probability of class 1 (positive)

#     # Combine and return as list of tuples
#     return predictions


# def run_batch_predict():
#     """
#     Runs prediction over images/test using the preprocess pipeline.
#     Returns a list of {file, true_label, pred_label, index, confidence}.
#     """
#     # 1) Features from preprocess
#     X_test, y_test, filenames, class_indices = get_test_features()

#     print(X_test)
#     print("Class:")
#     print(y_test)

#     chili_fusionnet = load_joblib("chili_fusionnet.joblib")
#     print("loaded")
#     # 3) Predict
#     y_idx = chili_fusionnet.predict(X_test)                        # (N,)
#     y_proba = chili_fusionnet.predict_proba(X_test).max(axis=1)    # (N,)

#     # 4) Decode labels
#     # class_map: index(str) -> label(str)
#     class_map       = load_json("class_map.json")
#     idx_to_label = lambda i: class_map.get(str(int(i)), str(int(i)))

#     pred_labels = [idx_to_label(i) for i in y_idx]
#     true_labels = [idx_to_label(i) for i in y_test]

#     # 5) Package results
#     results = []
#     for fn, t_lbl, p_lbl, idx, conf in zip(filenames, true_labels, pred_labels, y_idx, y_proba):
#         results.append({
#             "file": fn,
#             "true_label": t_lbl,
#             "pred_label": p_lbl,
#             "index": int(idx),
#             "confidence": float(conf)
#         })
#     return results


def run_single_predict(img_path):
    
    features = get_single_test_feature(img_path)
    print("Class:")

    chili_fusionnet = load_joblib("chili_fusionnet.joblib")
    print("loaded")
    # 3) Predict
    y_idx = chili_fusionnet.predict(features)                        # (N,)
    y_proba = chili_fusionnet.predict_proba(features).max(axis=1)    # (N,)

    # 4) Decode labels
    # class_map: index(str) -> label(str)
    class_map       = load_json("class_map.json")
    idx_to_label = lambda i: class_map.get(str(int(i)), str(int(i)))

    pred_labels = [idx_to_label(i) for i in y_idx]

    return {"predicted_label": pred_labels[0], "confidence" : float(y_proba[0])}