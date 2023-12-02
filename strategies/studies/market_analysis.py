import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class MarketAnalysis:
    def __init__(self, file_csv):
        self.file_csv = file_csv
        self.df = self.load_data()  # Stocke les données originales
        self.filtered_df = self.df  # Par défaut, utilise toutes les données

    # def load_data(self):
    #     df = pd.read_csv(self.file_csv)
    #     df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    #     return df

    def load_data(self):
        df = pd.read_csv(self.file_csv)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'],
                                         utc=True)  # Convertir en datetime avec prise en compte du fuseau horaire
        df['Timestamp'] = df['Timestamp'].dt.tz_convert(
            'Europe/Paris')  # Convertir dans un autre fuseau horaire si nécessaire
        return df

    # def set_time_interval(self, start_date=None, end_date=None):
    #     self.filtered_df = self.df  # Réinitialise à l'ensemble de données original
    #     if start_date:
    #         self.filtered_df = self.filtered_df[self.filtered_df['Timestamp'] >= pd.to_datetime(start_date)]
    #     if end_date:
    #         self.filtered_df = self.filtered_df[self.filtered_df['Timestamp'] <= pd.to_datetime(end_date)]

    def set_time_interval(self, start_date=None, end_date=None):
        self.filtered_df = self.df  # Réinitialise à l'ensemble de données original
        if start_date:
            start_date = pd.to_datetime(start_date).tz_localize(
                'Europe/Paris')  # Assurez-vous que la date de début est dans le même fuseau horaire
            self.filtered_df = self.filtered_df[self.filtered_df['Timestamp'] >= start_date]
        if end_date:
            end_date = pd.to_datetime(end_date).tz_localize(
                'Europe/Paris')  # Assurez-vous que la date de fin est dans le même fuseau horaire
            self.filtered_df = self.filtered_df[self.filtered_df['Timestamp'] <= end_date]

    def calculate_moving_averages(self, short_window=50, long_window=200):
        self.filtered_df['MA_Short'] = self.filtered_df['Close'].rolling(window=short_window).mean()
        self.filtered_df['MA_Long'] = self.filtered_df['Close'].rolling(window=long_window).mean()
        self.filtered_df['Trend'] = np.where(self.filtered_df['MA_Short']
                                             > self.filtered_df['MA_Long'],
                                             'Bullish', 'Bearish')

    def calculate_rsi(self, period=14):
        delta = self.filtered_df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        self.filtered_df['RSI'] = 100 - (100 / (1 + rs))

    def calculate_macd(self, slow=26, fast=12, signal=9):
        fast_ema = self.filtered_df['Close'].ewm(span=fast, adjust=False).mean()
        slow_ema = self.filtered_df['Close'].ewm(span=slow, adjust=False).mean()
        self.filtered_df['MACD'] = fast_ema - slow_ema
        self.filtered_df['MACD_Signal'] = self.filtered_df['MACD'].ewm(span=signal, adjust=False).mean()

    def calculate_volatility(self, window_size=20):
        self.filtered_df['Volatility'] = self.filtered_df['Close'].pct_change().rolling(
            window=window_size).std() * np.sqrt(window_size)

    def determine_entry_point(self):
        # Implementation depends on your entry strategy
        pass

    def calculate_stop_loss(self, window_size=20, multiplier=2):
        self.calculate_volatility(window_size)
        self.filtered_df['Stop_Loss'] = self.filtered_df['Close'] - (self.filtered_df['Volatility'] * multiplier)

    def plot_closes(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.filtered_df['Timestamp'], self.filtered_df['Close'], label='Close Price')

        # Obtenir la dernière valeur de stop loss
        last_stop_loss = self.filtered_df['Stop_Loss'].iloc[-1]

        # Ajouter une ligne horizontale pour le stop loss
        plt.axhline(y=last_stop_loss, color='r', linestyle='--', label='Stop Loss')

        plt.title('Close Price over Time')
        plt.xlabel('Timestamp')
        plt.ylabel('Close Price')
        plt.legend()
        plt.show()
    # def plot_closes(self):
    #     # Créer une figure avec plusieurs subplots
    #     fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1, 1]})
    #     fig.tight_layout(pad=3.0)
    #
    #     # Tracer les prix de clôture et les moyennes mobiles
    #     ax1.plot(self.filtered_df['Timestamp'], self.filtered_df['Close'], label='Close Price')
    #     ax1.plot(self.filtered_df['Timestamp'], self.filtered_df['MA_Short'], label='MA Short')
    #     ax1.plot(self.filtered_df['Timestamp'], self.filtered_df['MA_Long'], label='MA Long')
    #     ax1.set_title('Close Price and Moving Averages')
    #     ax1.set_ylabel('Price')
    #     ax1.legend()
    #
    #     # Tracer le MACD
    #     ax2.plot(self.filtered_df['Timestamp'], self.filtered_df['MACD'], label='MACD')
    #     ax2.plot(self.filtered_df['Timestamp'], self.filtered_df['MACD_Signal'], label='Signal')
    #     ax2.bar(self.filtered_df['Timestamp'], self.filtered_df['MACD'] - self.filtered_df['MACD_Signal'],
    #             label='Histogram', color='grey')
    #     ax2.set_title('MACD')
    #     ax2.set_ylabel('MACD')
    #     ax2.legend()
    #
    #     # Tracer le RSI
    #     ax3.plot(self.filtered_df['Timestamp'], self.filtered_df['RSI'], label='RSI')
    #     ax3.axhline(70, color='red', linestyle='dashed', linewidth=0.5)
    #     ax3.axhline(30, color='green', linestyle='dashed', linewidth=0.5)
    #     ax3.set_title('RSI')
    #     ax3.set_ylabel('RSI')
    #     ax3.set_xlabel('Timestamp')
    #     ax3.legend()
    #
    #     plt.show()

    def display_results(self, underlying_name):
        print("#### Underlying ####")
        print(underlying_name)

        print("\n#### Interval ####")
        start_date = self.filtered_df['Timestamp'].min().strftime('%Y-%m-%d %H:%M:%S')
        end_date = self.filtered_df['Timestamp'].max().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Start date: {start_date} > End date: {end_date}")

        print("\n#### Trend ####")
        trend = self.filtered_df['Trend'].iloc[-1]
        print("Trend is", "Bullish" if trend == 'Bullish' else "Bearish")

        print("\n#### RSI ####")
        print(self.filtered_df['RSI'].iloc[-1])

        print("\n#### MACD ####")
        print(f"MACD: {self.filtered_df['MACD'].iloc[-1]}, Signal: {self.filtered_df['MACD_Signal'].iloc[-1]}")

        print("\n#### VOLATILITY ####")
        print(self.filtered_df['Volatility'].iloc[-1])

        print("\n#### ENTRY PRICE ####")
        # A compléter selon votre stratégie d'entrée

        print("\n#### Last Close ####")
        last_close = self.filtered_df['Close'].iloc[-1]
        print(f"Last Close Price: {last_close}")

        print("\n#### STOP LOSS ####")
        print(self.filtered_df['Stop_Loss'].iloc[-1])


if __name__ == '__main__':
    # # Générer une série temporelle plus longue avec une tendance
    # dates = pd.date_range(start='20200101', periods=1000, freq='H')
    # trend = np.linspace(50, 150, len(dates))  # Tendance linéaire
    # noise = np.random.normal(0, 5, len(dates))  # Bruit aléatoire
    # close_prices = trend + noise
    #
    # # Générer 'Open', 'High', 'Low', 'Close', 'Volume'
    # data = {
    #     'Timestamp': dates,
    #     'Open': close_prices + np.random.normal(0, 2, len(dates)),
    #     'High': None,  # À remplir plus tard
    #     'Low': None,  # À remplir plus tard
    #     'Close': close_prices,
    #     'Volume': np.random.randint(100, 1000, len(dates))
    # }
    #
    # df = pd.DataFrame(data)
    # df['High'] = df[['Open', 'Close']].max(axis=1) + np.random.random(len(dates)) * 5
    # df['Low'] = df[['Open', 'Close']].min(axis=1) - np.random.random(len(dates)) * 5
    #
    # # Sauvegarder en CSV
    # df.to_csv('data.csv', index=False)

    analysis = MarketAnalysis('intra_2m_^BCBCLI.csv')
    analysis.set_time_interval(start_date='2023-11-09', end_date='2023-11-20')
    analysis.calculate_moving_averages()
    analysis.calculate_rsi()
    analysis.calculate_macd()
    analysis.calculate_volatility()
    analysis.calculate_stop_loss()
    analysis.display_results("BCBCLI")
    analysis.plot_closes()
