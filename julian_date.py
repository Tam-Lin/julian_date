#!/usr/bin/python3
# encoding: utf-8

import sys
from workflow import Workflow3, ICON_WEB
from datetime import date, timedelta, datetime
import operator

ops = {"+": operator.add, "-": operator.sub}

log = None

def main(wf):

	log.debug("Starting")

	log.debug(wf.args)

	from dateutil import parser

	args = wf.args

	today = datetime.timetuple(datetime.today())

	ddd = str(today.tm_yday).zfill(3)

	yyyyddd = str(today.tm_year) + ddd
	yyddd = str(today.tm_year)[2:] + ddd

	if len(args) == 0 or len(args[0]) == 0 or (len(args) == 1 and args[0] in ops):
	#No argument provided
	#today's date in Julian

		wf.add_item(title=yyyyddd, subtitle="Today's date -> yyyyddd", valid=True, arg=yyyyddd)
		wf.add_item(title=yyddd, subtitle="Today's date -> yyddd", valid=True, arg=yyddd)
		wf.add_item(title=ddd, subtitle="Today's date -> ddd", valid=True, arg=ddd )
		wf.send_feedback()

	else:

		if len(args) == 1:

			if args[0].isdigit() is True:

				date_input = args[0]

				if len(date_input) <= 3:  # assume format is ddd (current year)

					year = date.today().year
					day_of_year = int(date_input[:])

				elif len(date_input) == 4:  # assume format is yddd
					year = int(date_input[0:1])

					year = int(str((today.tm_year))[0:3] + str(year))

					day_of_year = int(date_input[1:])

				elif len(date_input) == 5:  # assume format is yyddd
					year = int(date_input[0:2])

					if year >= 50:
						year += 1900
					else:
						year += 2000

					day_of_year = int(date_input[2:])

				elif len(date_input) == 6:
					year = int(date_input[0:3])

					year = int(str((today.tm_year))[0:1] + str(year))

					day_of_year = int(date_input[3:])

				elif len(date_input) == 7:  # assume format is yyyyddd
					year = int(date_input[0:4])
					day_of_year = int(date_input[4:])

				else:
					year = None
					day_of_year = None

				if year != None:
					translated_date = date(year-1,12,31) + timedelta(days=day_of_year)
					#print translated_date
					wf.add_item(title=str(translated_date), subtitle="Year-Month-Day", valid=True, arg=str(translated_date))
					wf.send_feedback()

			elif args[0][0] in ops:
				#See http://stackoverflow.com/questions/1740726/python-turn-string-into-operator
				date_to_return = ops[args[0][0]](date.today(), timedelta(days=int(args[0][1:])))

				yyyyddd = str(date_to_return.timetuple().tm_year) + str(date_to_return.timetuple().tm_yday).zfill(3)

				wf.add_item(title = str(yyyyddd), subtitle="Today" + " " + args[0][0] + " " + args[0][1:].lstrip(), valid=True, arg=str(yyyyddd))
				wf.send_feedback()

			elif ('-' in args[0]) or ('/' in args[0]):

				input_date_object = None

				try:
					input_date_object = parser.parse(args[0])
				except:
					wf.add_item(title="Invalid entry", valid=False)
					wf.send_feedback()

				yyyyddd = str(input_date_object.timetuple().tm_year) + str(input_date_object.timetuple().tm_yday).zfill(3)

				wf.add_item(title = str(yyyyddd), subtitle=str(input_date_object.date()), valid=True, arg=str(yyyyddd))
				wf.send_feedback()


if __name__ == "__main__":
	# Create a global `Workflow3` object
	wf = Workflow3()
	# Call your entry function via `Workflow3.run()` to enable its
	# helper functions, like exception catching, ARGV normalization,
	# magic arguments etc.
	log = wf.logger
	sys.exit(wf.run(main))