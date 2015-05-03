import arrow


def time_estimator(parameters):
    time_per_run = 15
    no_of_runs = len(parameters)
    est_dur = time_per_run * no_of_runs
    nowtime = arrow.utcnow().to('US/Eastern')
    est_end = nowtime.replace(seconds=+est_dur)
    print 'We estimate that the optimization will be complete %s. [%s]' % (est_end.humanize(), est_end.format('h:mm A, MMM D, YYYY'))


def main():
    params=range(100000)
    time_estimator(params)

if __name__ == '__main__':
    main()
