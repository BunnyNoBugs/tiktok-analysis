import pandas as pd
import json
from fbprophet import Prophet
from orbit.diagnostics.plot import plot_predicted_data


class TikTokAnalyzer:
    def __init__(self, tiktoks, username=None):
        self.username = username
        self._tt_df = pd.DataFrame(tiktoks)
        self._tt_df['createTime'] = pd.to_datetime(self._tt_df['createTime'], unit='s').dt.date
        self._tt_df['likes'] = self._tt_df['stats'].apply(lambda x: x['diggCount'])
        self._tt_df['plays'] = self._tt_df['stats'].apply(lambda x: x['playCount'])

        self._data_df = pd.DataFrame(self._tt_df.groupby('createTime')['likes'].mean())
        self._data_df['plays'] = self._tt_df.groupby('createTime')['plays'].mean()
        self._data_df = self._data_df.reset_index()
        self._data_df = self._data_df.rename(columns={'createTime': 'ds'})

        self._plays_model = None
        self._likes_model = None

        self._likes_model_is_fitted = False
        self._plays_model_is_fitted = False

    def _fit_plays_model(self):
        plays_df = self._data_df.copy()
        plays_df = plays_df.rename(columns={'plays': 'y'})

        self._plays_model = Prophet()
        self._plays_model.fit(plays_df)

        self._plays_model_is_fitted = True

    def _fit_likes_model(self):
        likes_df = self._data_df.copy()
        likes_df = likes_df.rename(columns={'likes': 'y'})

        self._likes_model = Prophet()
        self._likes_model.add_regressor('plays')
        self._likes_model.fit(likes_df)

        self._likes_model_is_fitted = True

    def predict_likes(self, n_days=100):
        if not self._plays_model_is_fitted:
            self._fit_plays_model()
        if not self._likes_model_is_fitted:
            self._fit_likes_model()

        future_df = pd.DataFrame()
        future_df['ds'] = pd.date_range(start=self._data_df.iloc[-1]['ds'] + pd.Timedelta(days=1), periods=n_days)
        future_df['plays'] = self._plays_model.predict(future_df)['yhat']

        pred = self._likes_model.predict(future_df)

        return pred

    def plot_likes_prediction(self, pred, path: str = 'tmp/prediction.png'):
        pred = pred[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
        pred = pred.rename(columns={'yhat': 'prediction', 'yhat_lower': 'prediction_5', 'yhat_upper': 'prediction_95'})

        if self.username:
            plot_predicted_data(
                training_actual_df=self._data_df,
                predicted_df=pred,
                date_col='ds',
                actual_col='likes',
                insample_line=True,
                title=f'Average likes count per day prediction for TikTok user @{self.username}',
                is_visible=False,
                path=path
            )
        else:
            plot_predicted_data(
                training_actual_df=self._data_df,
                predicted_df=pred,
                date_col='ds',
                actual_col='likes',
                insample_line=True,
                title=f'Average TikTok likes count per day prediction',
                is_visible=False,
                path=path
            )


def main():
    with open('data/user_ghosthoney.json') as f:
        tiktoks = json.load(f)

    a = TikTokAnalyzer(tiktoks)
    pred = a.predict_likes()
    a.plot_likes_prediction(pred)


if __name__ == '__main__':
    main()
