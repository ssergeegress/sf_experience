import numpy as np
import pandas as pd
import plotly.express as px

def outliers_z_score(df: pd.DataFrame,
                     feature: pd.Series,
                     left: int = 3,
                     right: int = 3,
                     log_scale: bool = False,
                     shift: int = 0,
                     verb_info: bool = False) -> pd.DataFrame:
    """
    Функция принимает на вход датафрейм, наименование признака,
    целые числа, определяющие количества сигм для расчёта границ,\n
    булево значение для флага логарифмирования, целое число для
    смещения от нулевых значений при логарифмировании и флаг\n
    подробного вывода. Представляет из себя модификацию функции
    алгоритма метода z-отклонения (метода сигм).\n
    Помимо отсечения выбросов признака функция выводит по флагу
    информацию о вычисляемых значениях, показатель и сторону\n
    асимметрии, подробности о размерности возвращаемых фреймов,
    а также гистограмму распределения.\n
    Args:
        df (pd.DataFrame): Датафрейм
        feature (pd.Series): Признак
        left (int, optional): Сигмы слева. Defaults to 3
        right (int, optional): Сигмы справа. Defaults to 3
        log_scale (bool, optional): Флаг логарифмирования. Defaults to False
        shift (int, optional): Смещение от 0. Defaults to 0
        verb_info (bool, optional): Флаг подробностей. Defaults to False\n
    Returns:
        pd.DataFrame: Датафрейм с выбросами и "очищенный" датафрейм
    """
    if log_scale:
        df_here = np.log(df[feature] + shift)
    else:
        df_here = df[feature]
    mu = df_here.mean()
    sigma = df_here.std()
    lower_bound = mu - left * sigma
    upper_bound = mu + right * sigma
    asym = df_here.skew()

    fig = px.histogram(
        df_here,
        x=feature,
        # nbins=df[feature].unique().shape[0],
        title=f'Распределение признака {feature}. '
        f'Логарифмирование: {log_scale}.',
        width=800,
        height=500,
        marginal='box',
    )
    fig.add_vline(x=mu, line_width=2, line_dash="solid", line_color="red")
    fig.add_vline(x=lower_bound,
                  line_width=2,
                  line_dash="dash",
                  line_color="red")
    fig.add_vline(x=upper_bound,
                  line_width=2,
                  line_dash="dash",
                  line_color="red")
    fig.show()
    # fig.write_html("fig_04.html") # done (for github)

    outliers = df[(df_here < lower_bound) | (df_here > upper_bound)]
    cleaned = df[(df_here > lower_bound) & (df_here < upper_bound)]

    if verb_info:
        a, b = 'Правосторонняя', 'Левосторонняя'
        print(
            f'Математическое ожидание: {mu}, Стандартное отклонение: {sigma}\n'
            f'Нижняя граница: {lower_bound}, Верхняя граница: {upper_bound}\n'
            f'Асимметрия: {asym}, {a if asym > 0 else b}\n'
            f'Число выбросов по методу z-отклонения: {outliers.shape[0]}\n'
            f'Результирующее число записей: {cleaned.shape[0]}')

    return outliers, cleaned

if __name__ == '__main__':
    outliers_z_score()