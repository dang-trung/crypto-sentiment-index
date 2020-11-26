"""PCA-VAR Model.

Extract the first principal component of 9 sentiment indicators
"""
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from .visualize import plot_two_axis, plot_same_axis

if __name__ == '__main__':
    data = pd.read_csv("data/02_processed/final_dataset.csv", index_col='Date')
    # Independent Variables
    X = data.iloc[:, 1:]

    # Dependent Variable
    crix = data['CRIX']
    y = crix.diff() / crix.shift(1)
    y.rename('RET', inplace=True)
    y.dropna(inplace=True)

    # Create the Sentiment Index (First PC of all features)
    standard_X = StandardScaler().fit_transform(X.values)  # Standardize
    pca = PCA(n_components=1)
    PCA_X = pca.fit_transform(standard_X)
    PCA_X = pd.DataFrame(data=PCA_X, columns=['SENT'])
    PCA_X.index = X.index
    print(
        f"Explained Variance Ratio: "
        f"{round(pca.explained_variance_ratio_[0] * 100, 2)} %.")
    print(f"Loading Scores: {pca.components_}")

    # Plot CRIX versus SENT index
    crix_pca = pd.concat([crix, PCA_X], axis=1, join='inner')
    fig = plot_two_axis(data=crix_pca, series_1='CRIX', series_2='SENT',
                        name_series_1='CRIX', name_series_2='SENT')
    fig.show()
    fig.write_html('output/01_figures/fig.html')
    fig.write_image('output/01_figures/fig.svg')

    from statsmodels.tsa.api import VAR
    from statsmodels.tsa.stattools import adfuller


    def stationary(var, desc):
        """
        Print if it is true that a data series is stationary.

        Parameters
        ----------
        var : array-like, 1-d
        The data series to test stationarity.
        desc : str
        Name of the variable.

        Returns
        -------
        NoneType
        None
        """
        print(
            f"'{desc}' is stationary: "
            f"{adfuller(var)[0] < adfuller(var)[4]['1%']}.")
        print("---------------")


    stationary(PCA_X, 'SENT')  # SENT is not stationary
    X['DELTA SENT'] = PCA_X.diff()
    X.dropna(inplace=True)
    stationary(X['DELTA SENT'], 'DELTA SENT')  # DELTA SENT is stationary
    stationary(y, 'RET')  # RET is stationary

    # Fit stationary variables to VAR time series model
    Xy = pd.concat([y, X['DELTA SENT']], axis=1)

    # Ignore false warnings
    import warnings

    warnings.filterwarnings("ignore", message="A date index has been ")
    warnings.filterwarnings("ignore", message="The default dtype ")
    warnings.filterwarnings("ignore", category=UserWarning, module="pandas")

    model = VAR(Xy)
    result = model.fit(maxlags=15, ic='bic')
    result.summary()

    # Trading Strategy
    pred_ret = result.fittedvalues['RET']


    def signal(num):
        """
        Convert predicted returns into trading signals
        Parameters
        ----------
        num : int
            Any number (in our case predicted returns)

        Returns
        -------
        int
            Trading signals, depends on the signs of predicted returns
            (1 is go long, -1 is go short, 0 is stay still)

        """
        if num > 0:
            return 1
        elif num < 0:
            return -1
        else:
            return 0


    crix_pca = pd.concat([crix_pca, Xy], axis=1)
    crix_pca['SIGNAL'] = pred_ret.apply(signal)
    crix_pca['Cum Market Ret'] = (crix_pca['RET'] + 1).cumprod()
    crix_pca['Cum Strategy Ret'] = (
            crix_pca['RET'] * crix_pca['SIGNAL'] + 1).cumprod()
    strat = plot_same_axis(crix_pca, 'Cum Market Ret', 'Cum Strategy Ret',
                           'MARKET', 'STRATEGY')
    strat.show()
    strat.write_html('output/01_figures/strat.html')
    strat.write_image('output/01_figures/strat.svg')
