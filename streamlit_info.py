import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import scipy
import numpy as np

st.title('Визуализация данных о пассажирах с Титаника')

data = pd.read_csv('titanic.csv')

chart_type = st.selectbox('Выбери один из графиков:',['Диаграмма выживших для мужчин и женщин', 'Гистограмма стоимости билета', 'Гистограмма плотности возраста пассажиров', 'Круговая диаграмма порта посадки', 'Гистограмма средней стоимости поездки в разных классах'])

fig, ax = plt.subplots()

if chart_type == 'Диаграмма выживших для мужчин и женщин':
    gender = st.radio('Выберите пол:', ('Мужчины', 'Женщины', 'Все'), horizontal=True)
    if gender == 'Мужчины':
        male_data = [
            data[(data.Sex == 'male') & (data.Survived == 1)].Survived.count(),
            data[(data.Sex == 'male') & (data.Survived == 0)].Survived.count()
        ]


        bars = ax.bar(['Выжили', 'Погибли'], male_data,
                      color=['lightgreen', 'salmon'], width=0.6)

        ax.set_title('Выживаемость мужчин на Титанике', pad=20)
        ax.set_ylabel('Количество человек', labelpad=10)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{height}',
                    ha='center', va='bottom',
                    fontweight='bold')

    elif gender == 'Женщины':
        female_data = [
            data[(data.Sex == 'female') & (data.Survived == 1)].Survived.count(),
            data[(data.Sex == 'female') & (data.Survived == 0)].Survived.count()
        ]

        bars = ax.bar(['Выжили', 'Погибли'], female_data,
                      color=['lightgreen', 'salmon'], width=0.6)

        ax.set_title('Выживаемость женщин на Титанике', pad=20)
        ax.set_ylabel('Количество человек', labelpad=10)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{height}',
                    ha='center', va='bottom',
                    fontweight='bold')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='both', which='both', length=0)
    if gender == 'Все':
        female_survived = data[(data.Sex == 'female') & (data.Survived == 1)].Survived.count()
        female_died = data[(data.Sex == 'female') & (data.Survived == 0)].Survived.count()

        male_survived = data[(data.Sex == 'male') & (data.Survived == 1)].Survived.count()
        male_died = data[(data.Sex == 'male') & (data.Survived == 0)].Survived.count()

        x = ['Выжили', 'Погибли']
        bar_width = 0.35  # Ширина столбца

        bars1 = ax.bar([i - bar_width / 2 for i in range(len(x))],
                       [female_survived, female_died],
                       width=bar_width, label='Женщины', color='pink')

        bars2 = ax.bar([i + bar_width / 2 for i in range(len(x))],
                       [male_survived, male_died],
                       width=bar_width, label='Мужчины', color='lightblue')

        ax.set_title('Выживаемость по полу')
        ax.set_xticks(range(len(x)))
        ax.set_xticklabels(x)
        ax.set_ylabel('Количество человек')
        ax.legend()
        plt.grid(True)

        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2., height,
                        f'{int(height)}',
                        ha='center', va='bottom')

elif chart_type == 'Гистограмма стоимости билета':
    fares = data[data['Fare'] > 0].Fare
    ax.hist(fares, bins=30, color='skyblue', edgecolor='navy', alpha=0.7)


    ax.set_title('Распределение стоимости билетов', pad=15)
    ax.set_xlabel('Стоимость билета ($)', labelpad=10)
    ax.set_ylabel('Количество пассажиров', labelpad=10)

    ax.xaxis.set_major_formatter('${x:1.0f}')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.xticks(rotation=45, ha='right')

elif chart_type == 'Гистограмма плотности возраста пассажиров':
    ages = data[data['Age'] > 0].Age
    ax.hist(ages, bins=30, color='skyblue', edgecolor='navy', alpha=0.7, density = True)


    ages.plot(kind='kde', ax=ax, color='darkred',
              linewidth=2, label='KDE оценка')

    ax.set_title('Плотность возраста пассажирова', pad=15)
    ax.set_xlabel('Возраст пассажира', labelpad=10)
    ax.set_ylabel('Вероятность получить пассажира с таким возрастом', labelpad=10)

    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.xticks(rotation=45, ha='right')

elif chart_type == 'Круговая диаграмма порта посадки':
    port_counts = data['Embarked'].value_counts().dropna()

    colors = {
        'S': '#66b3ff',
        'C': '#ffcc99',
        'Q': '#99ff99'
    }

    # Создание диаграммы
    wedges, texts, autotexts = ax.pie(
        port_counts,
        colors=[colors[x] for x in port_counts.index],
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1},
        textprops={'fontsize': 12}
    )

    # Настройка подписей процентов
    plt.setp(autotexts, size=12, weight='bold', color='white')

    # Добавление легенды
    ax.legend(
        wedges,
        [f"{label} ({count})" for label, count in zip(
            ['Саутгемптон', 'Шербур', 'Квинстаун'],
            port_counts.values
        )],
        title="Порты посадки",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1)
    )

    # Заголовок
    ax.set_title('Распределение пассажиров по портам посадки', pad=20)

    # Делаем круг (чтобы не было сжатия)
    ax.axis('equal')

elif chart_type == 'Гистограмма средней стоимости поездки в разных классах':
    # Подготовка данных
    cost = data.groupby('Pclass')['Fare'].mean().sort_index()
    classes = ['1 класс', '2 класс', '3 класс']  # Красивые подписи

    # Настройка стиля
    colors = ['#4e79a7', '#f28e2b', '#e15759']  # Приятная цветовая палитра
    bar_width = 0.6  # Оптимальная ширина столбцов

    # Создание графика
    bars = ax.bar(classes, cost, width=bar_width, color=colors, edgecolor='white', linewidth=1)

    # Настройка оформления
    ax.set_title('Средняя стоимость билета по классам', pad=20, fontsize=14)
    ax.set_xlabel('Класс обслуживания', labelpad=10)
    ax.set_ylabel('Средняя стоимость ($)', labelpad=10)

    # Форматирование оси Y (денежный формат)
    ax.yaxis.set_major_formatter('${x:,.0f}')

    # Добавление значений над столбцами
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height,
                f'${height:,.1f}',
                ha='center', va='bottom',
                fontsize=11)

    # Удаление лишних элементов
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Настройка сетки
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    # Автоматическая подгонка высоты оси Y
    ax.set_ylim(0, cost.max() * 1.15)  # +15% от максимального значения

st.pyplot(fig)




if st.checkbox('Показать исходные данные'):
    n_rows = st.number_input(
        'Количество строк для отображения',
        min_value=1,
        max_value=len(data),
        value=min(10, len(data)),
        step=1
    )
    st.write(data.head(n_rows))
    st.caption(f"Всего строк в данных: {len(data)}")