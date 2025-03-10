import telebot
import io
import matplotlib.pyplot as plt

from DAO.dao_controller import DaoController as Dao


class GraphController:
    def pie_chart(self, user_id:int, date:telebot.types.Message) -> io.BytesIO | None:
        data = Dao().get_foods_by_user_and_date(user_id, date)
        if not data:
            return None

        labels = ['total_fat', 'cholesterol', 'sodium', 'total_carbohydrate', 'potassium', 'protein', 'sugars']
        details = {}

        for label in labels:
            details[label] = .0

        for food in data:
            details['total_fat'] += float(food['total_fat'].split()[0])
            details['cholesterol'] += float(food['cholesterol'].split()[0])
            details['sodium'] += float(food['sodium'].split()[0])
            details['total_carbohydrate'] += float(food['total_carbohydrate'].split()[0])
            details['potassium'] += float(food['potassium'].split()[0])
            details['protein'] += float(food['protein'].split()[0])
            details['sugars'] += float(food['sugars'].split()[0])

        details['cholesterol'] /= 1000
        details['sodium'] /= 1000
        details['potassium'] /= 1000

        values = list(details.values())
        total = sum(values)
        percentages = [f'{(value / total) * 100:.1f}%' for value in values]
        legend_labels = [f'{label}: {percentage}' for label, percentage in zip(labels, percentages)]

        fig, ax = plt.subplots()
        ax.pie(values, startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title(f"User Nutritions Details for {date.text}")
        ax.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0.5))

        # Save the plot to an in-memory buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)     # Go to the start of the stream

        plt.close(fig)
        return buf

    def bar_chart(self, user_id:int, date:telebot.types.Message) -> io.BytesIO | None:
        data = Dao().get_foods_by_user_and_date(user_id, date)
        if not data:
            return None

        chart_data = {}
        for food in data:
            if food['name'] not in chart_data:
                chart_data[food['name']] = [.0, 0]   # [total_calories, count]
            chart_data[food['name']][0] += float(food['calories'])
            chart_data[food['name']][1] += 1
        labels = list(chart_data.keys())
        values = [value[0] for value in chart_data.values()]
        amounts = [value[1] for value in chart_data.values()]

        fig, ax = plt.subplots()
        bars = ax.bar(labels, values)
        ax.set_ylabel('Calories')
        ax.set_xlabel('Meal')
        ax.set_title(f"User Calories Details for {date.text}")

        # add numeral texts for each bar
        for bar, amount in zip(bars, amounts):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f'{height:.1f}',
                ha='center',
                va='bottom'
            )
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height / 2 - 10,    # 10 is the approximate height of the text / 2
                f'x{amount}',
                ha='center',
                va='bottom'
            )

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)

        plt.close(fig)
        return buf
