import unittest
import sys
sys.path.append('../dmit/')
import datetime as dt

from datetools import round_time
from datetools import current_run_datetime
from datetools import month_delta

class TestDateTools(unittest.TestCase):

    def test_round_time_down(self):
        self.assertEqual(round_time(dt=dt.datetime(2020,1,1,0,20), 
                                    roundTo=dt.timedelta(minutes=60), 
                                    roundType='rounddown'), 
                                    dt.datetime(2020,1,1,0,0))

    def test_round_time_up(self):
        self.assertEqual(round_time(dt=dt.datetime(2020,1,1,0,20), 
                                    roundTo=dt.timedelta(minutes=60), 
                                    roundType='roundup'), 
                                    dt.datetime(2020,1,1,1,0))

    def test_round_time_nearest(self):
        self.assertEqual(round_time(dt=dt.datetime(2020,1,1,0,20), 
                                    roundTo=dt.timedelta(minutes=60), 
                                    roundType='nearest'), 
                                    dt.datetime(2020,1,1,0,0))

    def test_month_delta(self):
        self.assertEqual(month_delta(dt.datetime(2020,1,1,12), dt.datetime(2020,10,2,0)), 
                                    9)

    def test_current_run(self):
        self.assertEqual(current_run_datetime(frequency=180, delay=120, now=dt.datetime(2020,1,1,12)), 
                                    dt.datetime(2020,1,1,9))

        self.assertEqual(current_run_datetime(frequency=180, delay=120, now=dt.datetime(2020,1,1,13)), 
                                    dt.datetime(2020,1,1,9))
        
        self.assertEqual(current_run_datetime(frequency=180, delay=120, now=dt.datetime(2020,1,1,13,10)), 
                                    dt.datetime(2020,1,1,9))
        
        self.assertEqual(current_run_datetime(frequency=180, delay=120, now=dt.datetime(2020,1,1,13,59)), 
                                    dt.datetime(2020,1,1,9))

        self.assertEqual(current_run_datetime(frequency=180, delay=120, now=dt.datetime(2020,1,1,14,0)), 
                                    dt.datetime(2020,1,1,12))

        self.assertEqual(current_run_datetime(frequency=180, delay=10, now=dt.datetime(2020,1,1,12,5)), 
                                    dt.datetime(2020,1,1,9))

        self.assertEqual(current_run_datetime(frequency=180, delay=120, now=dt.datetime(2020,1,1,13,59)), 
                                    dt.datetime(2020,1,1,9))

        self.assertEqual(current_run_datetime(frequency=60, delay=10, now=dt.datetime(2020,1,1,12,5)), 
                                    dt.datetime(2020,1,1,11,0))

        self.assertEqual(current_run_datetime(frequency=10, delay=10, now=dt.datetime(2020,1,1,12,5)), 
                                    dt.datetime(2020,1,1,11,50))

        self.assertEqual(current_run_datetime(frequency=10, delay=10, now=dt.datetime(2020,1,1,12,55), roundto='minute'), 
                                    dt.datetime(2020,1,1,12,40))

        self.assertEqual(current_run_datetime(frequency=10, delay=10, now=dt.datetime(2020,1,2,0,5), roundto='minute'), 
                                    dt.datetime(2020,1,1,23,50))

        self.assertEqual(current_run_datetime(frequency=10, delay=10, now=dt.datetime(2021,1,1,0,5), roundto='minute'), 
                                    dt.datetime(2020,12,31,23,50))

        self.assertEqual(current_run_datetime(frequency=10, delay=20, now=dt.datetime(2020,1,1,12,40), roundto='minute'), 
                                    dt.datetime(2020,1,1,12,20))

        self.assertEqual(current_run_datetime(frequency=30, delay=5, now=dt.datetime(2020,1,1,12,40), roundto='minute'), 
                                    dt.datetime(2020,1,1,12,30))

        self.assertEqual(current_run_datetime(frequency=60, delay=60, now=dt.datetime(2020,1,1,12,40), roundto='minute'), 
                                    dt.datetime(2020,1,1,11,0))


# class lflslfslflslfslfs(unittest.TestCase):

#     def test_month_delta(self):
#         self.assertEqual(month_delta(dt.datetime(2020,1,1,12), dt.datetime(2020,10,2,0)), 
#                                     9)


if __name__=="__main__":
    unittest.main()