from PyPDF2 import PdfReader

reader = PdfReader('statement-2022-11.pdf')
start_parsing = 'Description Booking Date Amount'
stop_parsing = 'Bank Statement Nr.'
lines = []
for page in reader.pages:
    text = page.extract_text()
    started = False
    for line in text.split('\n'):
        if start_parsing in line:
            started = True
            continue
        if stop_parsing in line:
            line = line[:line.index(stop_parsing)]
            lines.append(line)
            break
        if started:
            lines.append(line)

n = 3
data = [lines[i:i + n] for i in range(0, len(lines), n)]

class Transaction:
    def __init__(self, lst: list[str]):
        self.name: str = lst[0]
        self.type: str = (lst[1].split('•')[1] if len(lst[1].split('•')) == 2 else 'Unspecified').lstrip()
        date: str = lst[2].split(' ')[2]
        self.date = date[:int(len(date) / 2)]
        price = lst[2].split(' ')[3]
        self.price: float = float(price[:-1].replace(',', '.'))

    def __repr__(self):
        return f'{self.name}; {self.type}; {self.price}; {self.date}'

data = list(map(lambda x : Transaction(x), data))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

# hide axes
# fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')

types = list(set(map(lambda t : t.type, data)))

types_sum = list(map(lambda type : sum(map(lambda t : t.price, filter(lambda t : t.type == type, data))), types))

df = pd.DataFrame(types_sum, index=types, columns=['Total'])

the_table = ax.table(cellText=list(zip(types, df.values)), colLabels=['Type'] + list(df.columns), loc='center')
the_table.auto_set_font_size(False)
the_table.set_fontsize(10)

fig.tight_layout()

plt.show()
