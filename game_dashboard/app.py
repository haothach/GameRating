import streamlit as st
import joblib
import numpy as np
import pandas as pd
from datetime import datetime

# ======= Load mô hình và encoders =======
model = joblib.load("model/xgb_model_rating.pkl")
mlb_genres = joblib.load("model/mlb_genres.pkl")
mlb_platforms = joblib.load("model/mlb_platforms.pkl")
mlb_tags = joblib.load("model/mlb_tags.pkl")
expected_feature_names = joblib.load("model/expected_feature_names.pkl")  # Danh sách cột đúng

# ======= Map nhãn phân loại =======
label_map = {
    0: "Rating thấp (1–3.3)",
    1: "Rating Cao (3.3–5)"
}

# ======= Giao diện =======
st.set_page_config(page_title="Dự đoán Rating Game", layout="centered")
st.title("Dự đoán Rating Game")
st.markdown("Hãy nhập thông tin game để hệ thống dự đoán nhóm rating.")

# ======= Nhập input người dùng =======
playtime = st.slider("Thời gian chơi trung bình (playtime)", 0, 200, 50)
year = st.number_input("Năm phát hành game", min_value=1980, max_value=2025, value=2020)
added = st.number_input("Số người thêm vào danh sách (added)", min_value=0)
ratings_count = st.number_input("Số lượng đánh giá (ratings_count)", min_value=0)
reviews_count = st.number_input("Số lượng review (reviews_count)", min_value=0)

platform_input = st.multiselect("Nền tảng", mlb_platforms.classes_)
genre_input = st.multiselect("Thể loại", mlb_genres.classes_)
tag_input = st.multiselect("Tag (tuỳ chọn)", mlb_tags.classes_)

# ======= Đặc trưng phụ =======
platform_count = len(platform_input)
genre_count = len(genre_input)
tag_count = len(tag_input)
is_multiplatform = 1 if platform_count > 1 else 0
age_of_game = datetime.now().year - year
review_ratio = ratings_count / reviews_count if reviews_count > 0 else 0
log_playtime = np.log1p(playtime)
log_added = np.log1p(added)
log_reviews_count = np.log1p(reviews_count)
log_ratings_count = np.log1p(ratings_count)

# ======= Numeric features =======
numeric_features = np.array([[year, added, playtime, ratings_count, reviews_count,
                              platform_count, genre_count, tag_count, is_multiplatform,
                              age_of_game]])  # 12 cột


numeric_feature_names = [
    'year', 'added', 'playtime', 'ratings_count', 'reviews_count',
    'platform_count', 'genre_count', 'tag_count', 'is_multiplatform',
    'age_of_game'
]



# ======= Encode các feature đa lựa chọn =======
genre_ohe = mlb_genres.transform([genre_input])
platform_ohe = mlb_platforms.transform([platform_input])
tag_ohe = mlb_tags.transform([tag_input])

genre_names = list(mlb_genres.classes_)
platform_names = list(mlb_platforms.classes_)
tag_names = list(mlb_tags.classes_)

# ======= Gộp toàn bộ thành dataframe có tên cột =======
X_input = np.hstack([numeric_features, genre_ohe, platform_ohe, tag_ohe])
input_feature_names = numeric_feature_names + genre_names + platform_names + tag_names
X_input_df = pd.DataFrame(X_input, columns=input_feature_names)

# ======= So sánh cột với mô hình gốc =======
expected_set = set(expected_feature_names)
input_set = set(input_feature_names)

extra_columns = sorted(list(input_set - expected_set))
missing_columns = sorted(list(expected_set - input_set))


# ======= Dự đoán nếu đủ =======
if st.button("Dự đoán"):
    if extra_columns or missing_columns:
        st.error("Không thể dự đoán do mismatch số lượng cột. Vui lòng kiểm tra lại.")
    else:
        # Đảm bảo đúng thứ tự và dùng đúng biến
        X_input_df = pd.DataFrame(0, index=[0], columns=expected_feature_names)
        for col in expected_feature_names:
            if col in input_feature_names:
                idx = input_feature_names.index(col)
                X_input_df[col] = X_input[0][idx]

        proba = model.predict_proba(X_input_df.values)[0]
        prediction = np.argmax(proba)
        st.write(f"Xác suất dự đoán: {proba}")
        st.success(f"Kết quả dự đoán: {label_map[prediction]}")

