from flask import Flask, render_template, request
import pandas as pd
from sklearn.calibration import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

app = Flask(__name__)

# Load and preprocess data
df = pd.read_csv('skincare.csv')

le_skin_type = LabelEncoder()
df['SkinTypeLabel'] = le_skin_type.fit_transform(df['Skin_Type'])

skin_types = ['SkinTypeLabel']
X = df[skin_types] 
y = df['SkinTypeLabel']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

@app.route('/')
def index():
    skin_types = sorted(df['Skin_Type'].unique())
    return render_template('recommendation_form.html', skin_types=skin_types)

@app.route('/recommend', methods=['POST'])
def recommend():
    skin_type = request.form['skin_type']
    
    df_query = pd.DataFrame({'SkinTypeLabel': [df[df['Skin_Type'] == skin_type]['SkinTypeLabel'].iloc[0]]})
    predictions = clf.predict(df_query)
    
    recommended_products = df[df['SkinTypeLabel'] == predictions[0]].head(10).to_dict(orient='records')

    return render_template('recommandation_product.html', skin_type=skin_type, products=recommended_products, accuracy=accuracy)

if __name__ == '__main__':
    app.run(debug=True)
