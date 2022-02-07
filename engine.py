from PyQt5.QtWidgets import QMessageBox
import sqlite3 as sql
import pandas as pd

class Inference:
    def __init__(self):
        super(Inference, self).__init__()
        self.knowledge_base_path = r'database.db'
        self.db = sql.connect(self.knowledge_base_path)
        self.c = self.db.cursor()
        self.df_con1 = pd.read_csv(r'conditions\inference_table_con1.csv')
        self.df_con2 = pd.read_csv(r'conditions\inference_table_con2.csv')
        self.df_con3 = pd.read_csv(r'conditions\inference_table_con3.csv')
        self.df_con4 = pd.read_csv(r'conditions\inference_table_con4.csv')
        self.df_con5 = pd.read_csv(r'conditions\inference_table_con5.csv')
        self.df_con6 = pd.read_csv(r'conditions\inference_table_con6.csv')
        self.strategies = pd.read_csv(r'conditions\strategies.csv')

    def combo_parser(self, _choise):

        if _choise == 0:
            return "A"

        if _choise == 1:
            return "B"

        if _choise == 2:
            return "C"

    def condition1_func(self, sales_income, target_sales):

        devision = sales_income / target_sales

        if devision >= 0.95:
            return 'A'

        if (devision < 0.95) and (devision >= 0.75):
            return 'B'

        if devision < 0.75:
            return 'C'

    def condition2_func(self, sales_rate):

        if sales_rate > 125:
            return 'A'

        if (sales_rate < 125) and (sales_rate >= 85):
            return 'B'

        if sales_rate < 85:
            return 'C'

    def condition3_func(self, visitor_num, customer_num):
        vis_rate = customer_num / visitor_num

        if vis_rate > 0.5:
            return 'A'

        if (vis_rate < 0.5) and (vis_rate >= 0.1):
            return 'B'

        if vis_rate < 0.1:
            return 'C'

    def condition4_func(self, con2, con3):
        if con2 == 'A' and con3 == 'A':
            return 'A'

        if con2 == 'A' and con3 == 'B':
            return 'A'

        if con2 == 'A' and con3 == 'C':
            return 'A'

        if con2 == 'B' and con3 == 'A':
            return 'A'

        if con2 == 'B' and con3 == 'B':
            return 'B'

        if con2 == 'B' and con3 == 'C':
            return 'C'

        if con2 == 'C' and con3 == 'A':
            return 'A'

        if con2 == 'C' and con3 == 'B':
            return 'B'

        if con2 == 'C' and con3 == 'C':
            return 'C'

    def condition5_func(self, market_share):
        if market_share > 0.3:
            return 'A'

        if (market_share < 0.3) and (market_share >= 0.1):
            return 'B'

        if market_share < 0.1:
            return 'C'

    def knowledgebase_inference(self, _saleslevel, _salesrate, _captivatelevel,
                                _captivaterate, _compatitor, _future):


        self.c.execute('SELECT result FROM rules WHERE '
                  'saleslevel = "{}" AND '
                  'salesrate = "{}" AND '
                  'captivatelevel = "{}" AND '
                  'captivaterate = "{}" AND '
                  'compatitor = "{}" AND '
                  'future = "{}"'.format(_saleslevel, _salesrate, _captivatelevel,
                  _captivaterate, _compatitor, _future))

        rows = self.c.fetchall()
        self.db.commit()
        # self.db.close()
        if len(rows) == 0:
            return None
        else:
            return rows[0][0]

    def knowledgebase_edit(self, _saleslevel, _salesrate, _captivatelevel,
                                _captivaterate, _compatitor, _future):


        self.c.execute('SELECT * FROM rules WHERE '
                  'saleslevel = "{}" AND '
                  'salesrate = "{}" AND '
                  'captivatelevel = "{}" AND '
                  'captivaterate = "{}" AND '
                  'compatitor = "{}" AND '
                  'future = "{}"'.format(_saleslevel, _salesrate, _captivatelevel,
                  _captivaterate, _compatitor, _future))

        rows = self.c.fetchall()
        self.db.commit()
        # self.db.close()
        if len(rows) == 0:
            return None
        else:
            return rows[0][0]

    def scoring_engine(self, condition_1, condition_2,
                         condition_3, condition_4,
                         condition_5, condition_6):

        strategy_score = dict()
        for s_index in range(0, 20):
            strategy_score[str(s_index)] = self.df_con1.iloc[s_index][condition_1]

        for s_index in range(0, 20):
            strategy_score[str(s_index)] += self.df_con2.iloc[s_index][condition_2]

        for s_index in range(0, 20):
            strategy_score[str(s_index)] += self.df_con3.iloc[s_index][condition_3]

        for s_index in range(0, 20):
            strategy_score[str(s_index)] += self.df_con4.iloc[s_index][condition_4]

        for s_index in range(0, 20):
            strategy_score[str(s_index)] += self.df_con5.iloc[s_index][condition_5]

        for s_index in range(0, 20):
            strategy_score[str(s_index)] += self.df_con6.iloc[s_index][condition_6]

        total_scores = 0
        for item in range(0, 19):
            total_scores += strategy_score[str(item)]

        strategy_score = {k: v / total_scores for k, v in strategy_score.items()}
        not_sorted_output = strategy_score
        strategy_score = {k: v for k, v in sorted(strategy_score.items(), key=lambda item: item[1])}
        # print(strategy_score)
        # print(not_sorted_output)
        return strategy_score, not_sorted_output

    def validate_input(self, sales_income, target_sales,
                       sales_rate, visitor_num,
                       customers_num, market_share,
                       future_combo):

        sales_income = float(sales_income)
        target_sales = float(target_sales)
        sales_rate = float(sales_rate)
        visitor_num = int(visitor_num)
        customers_num = int(customers_num)
        market_share = float(market_share)
        future_combo = int(future_combo)
        if market_share > 100:
            market_share = 100
        return [sales_income, target_sales, sales_rate, visitor_num, customers_num, market_share, future_combo]

    def inference_engine(self, sales_income, target_sales,
                         sales_rate, visitor_num,
                         customers_num, market_share,
                         future_combo):
        try:
            values_list = self.validate_input(sales_income,
                                target_sales,
                                sales_rate,
                                visitor_num,
                                customers_num,
                                market_share,
                                future_combo)

            condition_1 = self.condition1_func(values_list[0], values_list[1])
            condition_2 = self.condition2_func(values_list[2])
            condition_3 = self.condition3_func(values_list[3], values_list[4])
            condition_4 = self.condition4_func(condition_2, condition_3)
            condition_5 = self.condition5_func(values_list[5])
            condition_6 = self.combo_parser(values_list[6])

            exact_output = self.knowledgebase_inference(condition_1,
                                                        condition_2,
                                                        condition_3,
                                                        condition_4,
                                                        condition_5,
                                                        condition_6)

            engine_output, not_sorted_output = self.scoring_engine(condition_1,
                                                  condition_2,
                                                  condition_3,
                                                  condition_4,
                                                  condition_5,
                                                  condition_6)

            top_strategy_index = list(engine_output)[-1]
            top_strategy = self.strategies.iloc[int(top_strategy_index)][0]

            return engine_output, top_strategy, exact_output, not_sorted_output
        except:

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText('اطلاعات ورودی صحیح نمیباشد لطفا در ارائه اطلاعات دقت فرمایید')
            msg.setWindowTitle("خطا در ورودی")
            retval = msg.exec_()
            return None, None, None

    def insert_new_rule(self, sales_income, target_sales,
                         sales_rate, visitor_num,
                         customers_num, market_share,
                         future_combo, new_result):
        try:
            values_list = self.validate_input(sales_income,
                                target_sales,
                                sales_rate,
                                visitor_num,
                                customers_num,
                                market_share,
                                future_combo)

            condition_1 = self.condition1_func(values_list[0], values_list[1])
            condition_2 = self.condition2_func(values_list[2])
            condition_3 = self.condition3_func(values_list[3], values_list[4])
            condition_4 = self.condition4_func(condition_2, condition_3)
            condition_5 = self.condition5_func(values_list[5])
            condition_6 = self.combo_parser(values_list[6])
            self.insert_rule_db(condition_1,
                                condition_2,
                                condition_3,
                                condition_4,
                                condition_5,
                                condition_6,
                                new_result)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText('قانون با موفقیت ثبت شد')
            msg.setWindowTitle("ثبت")
            retval = msg.exec_()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText('اطلاعات ورودی صحیح نمیباشد لطفا در ارائه اطلاعات دقت فرمایید')
            msg.setWindowTitle("خطا در ورودی")
            retval = msg.exec_()
            return None, None, None


    def edit_rule(self, sales_income, target_sales,
                         sales_rate, visitor_num,
                         customers_num, market_share,
                         future_combo, new_result):
        try:
            values_list = self.validate_input(sales_income,
                                target_sales,
                                sales_rate,
                                visitor_num,
                                customers_num,
                                market_share,
                                future_combo)

            condition_1 = self.condition1_func(values_list[0], values_list[1])
            condition_2 = self.condition2_func(values_list[2])
            condition_3 = self.condition3_func(values_list[3], values_list[4])
            condition_4 = self.condition4_func(condition_2, condition_3)
            condition_5 = self.condition5_func(values_list[5])
            condition_6 = self.combo_parser(values_list[6])
            exact_output = self.knowledgebase_edit(condition_1,
                                                   condition_2,
                                                   condition_3,
                                                   condition_4,
                                                   condition_5,
                                                  condition_6)

            if exact_output == None:
                self.c.execute('SELECT * From rules;')
                rows = self.c.fetchall()
                self.c.execute('INSERT INTO rules VALUES (?, ?, ?, ?, ?, ?, ?, ?)', [len(rows) - 1, condition_1, condition_2,
                                                                                condition_3, condition_4,
                                                                                condition_5, condition_6, new_result])
                self.db.commit()
                # self.db.close()
            if exact_output != None:
                self.c.execute('UPDATE rules SET result = "{}" WHERE rowid = {}'.format(new_result, exact_output + 1))
                self.db.commit()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText('قانون با موفقیت ویرایش شد')
            msg.setWindowTitle("ویرایش")
            retval = msg.exec_()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText('اطلاعات ورودی صحیح نمیباشد لطفا در ارائه اطلاعات دقت فرمایید')
            msg.setWindowTitle("خطا در ورودی")
            retval = msg.exec_()

    def insert_rule_db(self, condition_1, condition_2, condition_3, condition_4, condition_5, condition_6, result):

        self.c.execute('SELECT * From rules;')
        rows = self.c.fetchall()
        last = rows.pop()

        self.c.execute('INSERT INTO rules VALUES (?, ?, ?, ?, ?, ?, ?, ?)', [last[0] + 1, condition_1, condition_2,
                                                                        condition_3, condition_4,
                                                                        condition_5, condition_6, result])

        self.db.commit()
        # self.db.close()
