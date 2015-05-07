from django.core.management.base import BaseCommand
#from django.core.management.base import BaseCommand, CommandError

import csv
from collections import Counter, defaultdict
from itertools import product

DIFFICULTIES_FILE = 'data/difficulties.csv'
STEP = 0.5


def process_difficulties_data():
    questions_correct = Counter()
    questions_total = Counter()
    with open(DIFFICULTIES_FILE, 'r') as f:
        csvreader = csv.reader(f, delimiter=';')
        # skip header
        next(csvreader)
        for row in csvreader:
            difficulty = float(row[0])
            group = int((2 + difficulty) / STEP)
            correct = int(row[1])
            questions_correct[group] += correct
            questions_total[group] += 1
            #print difficulty, correct, type(difficulty), type(correct)
        print '\nDifficulties:'
        for group in range(int(4 / STEP)):
            min_difficutly = -2 + group * STEP
            success_rate = float(questions_correct[group]) / questions_total[group]
            print group, min_difficutly, success_rate, questions_total[group]


class Command(BaseCommand):
    args = '<data_file_name>'
    help = 'Print statistics on the standard output and creates graphs.'

    def handle(self, *args, **options):
        if len(args) > 0:
            data_file_name = args[0]
        else:
            data_file_name = 'data/data.csv'

        with open(data_file_name, 'r') as f:
            csvreader = csv.reader(f, delimiter=';')
            # skip header
            next(csvreader)
            # echa row is ['{sid}', '{kb}', '{ec}', '{eg}', '{pr}',
            # '{correct}', '{wrong}', '{unanswered}', '{invalid}', '{irrelevant}',
            # '{final_rating:.1f}', '{performance:.5f}', '{topic}'
            counter = Counter()
            performances = defaultdict(list)
            for row in csvreader:
                print row

                # read all information
                #sid = int(row[0])
                kb = int(row[1])
                ec = int(row[2])
                eg = int(row[3])
                pr = int(row[4])
                correct = int(row[5])
                wrong = int(row[6])
                unanswered = int(row[7])
                invalid = int(row[8])
                irrelevant = int(row[9])
                final_rating = float(row[10])
                performance = float(row[11])
                #topic = row[12]

                counter['session'] += 1
                counter['correct'] += correct
                counter['wrong'] += wrong
                counter['unanswered'] += unanswered
                counter['invalid'] += invalid
                counter['irrelevant'] += irrelevant
                counter['final_rating_good'] += int(final_rating > 0.6)
                counter['final_rating_soso'] += int(0.4 < final_rating < 0.6)
                counter['final_rating_bad'] += int(final_rating < 0.4)
                counter['performance'] += performance

                if correct + wrong + unanswered >= 3:
                    performances[(kb, ec, eg, pr)].append(performance)

        # smoothing: add one made up session with average performance
        components_lists = [[2, 3], [1], [1], [1, 2, 3, 4, 5, 6]]
        AVERAGE_PERFORMANCE = 0.5
        for components_keys in product(*components_lists):
            performances[tuple(components_keys)].append(AVERAGE_PERFORMANCE)

        # transform to list and shrink to average number for a components-combo
        performances_list = []
        for components_keys in performances:
            component_performances = performances[components_keys]
            performance = sum(component_performances) / len(component_performances)
            performance_record = list(components_keys)
            performance_record.append(performance)
            performances_list.append(performance_record)

        # calculate performances of single compoents
        kb_performances = defaultdict(int)
        pr_performances = defaultdict(int)
        for record in performances_list:
            kb_performances[record[0]] += record[4]
            pr_performances[record[3]] += record[4]
        kb_performances = {k: p / 6 for (k, p) in kb_performances.items()}
        pr_performances = {k: p / 2 for (k, p) in pr_performances.items()}

        # calculate global statisctics
        sessions = counter['session']
        correct, wrong, unanswered = counter['correct'], counter['wrong'], counter['unanswered']
        invlaid, irrelevant = counter['invalid'], counter['irrelevant']
        questions = correct + wrong + unanswered
        ok_questions = questions - invalid - irrelevant
        average_success = float(correct) / (correct + wrong)
        average_performance = counter['performance'] / sessions

        # print the statistics
        report_format = '''
sessions: {sessions}
questions: {questions}
correct/wrong/unanswered: {correct}/{wrong}/{unanswered}
average success: {average_success}
ok/invalid/irrelevant: {ok}/{invalid}/{irrelevant}
final-good/so-so/bad: {final_good}/{final_soso}/{final_bad}
average performance: {average_performance} (RELATIVE performnace!)
kb performance 2/3: {kb2performance}/{kb3performance}
pr performance 1/../6: {pr1}/{pr2}/{pr3}/{pr4}/{pr5}/{pr6}
'''
        print report_format.format(
            sessions=sessions,
            questions=questions,
            correct=correct,
            wrong=wrong,
            unanswered=unanswered,
            average_success=average_success,
            ok=ok_questions,
            invalid=invalid,
            irrelevant=irrelevant,
            final_good=counter['final_rating_good'],
            final_soso=counter['final_rating_soso'],
            final_bad=counter['final_rating_bad'],
            average_performance=average_performance,
            kb2performance=kb_performances[2],
            kb3performance=kb_performances[3],
            pr1=pr_performances[1],
            pr2=pr_performances[2],
            pr3=pr_performances[3],
            pr4=pr_performances[4],
            pr5=pr_performances[5],
            pr6=pr_performances[6]
        )

        print 'Performance list:'
        for performance_record in performances_list:
            print performance_record

        #process_difficulties_data()
