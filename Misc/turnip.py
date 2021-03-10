#turnip.py

class Const:
	TURNIP_INVENTORY_STACK = 100
	TURNIP_HIGH_PRICE      = 660
	TURNIP_PROFIT_START    = 120

class TaskType:
	TURNIP_HELP        = 'th'
	TURNIP_COUNT       = 'tc'
	TURNIP_SELL_PRICE  = 'tsp'
	TURNIP_BOUGHT      = 'tb'
	TURNIP_PROFIT      = 'tp'
	TURNIP_TABLE       = 'tt'
	TURNIP_LOSS        = 'tl'

class CommandLineKeys:
	TASK       = '-tk'
	BUY_PRICE  = '-bp'
	SELL_PRICE = '-sp'
	PROFIT     = '-p'
	STACKS     = '-s'
	TURNIPS    = '-t'
	STEP_SIZE  = '-ss'
	BELLS      = '-bll'

parameter_help = {
	CommandLineKeys.TASK       : 'Task program executes',
	CommandLineKeys.BUY_PRICE  : 'Price of turnips when bought',
	CommandLineKeys.SELL_PRICE : 'Price of turnips when sold',
	CommandLineKeys.PROFIT     : 'Profit made from turnips',
	CommandLineKeys.STACKS     : 'Turnip inventory stacks of 100',
	CommandLineKeys.TURNIPS    : 'Number of turnips',
	CommandLineKeys.STEP_SIZE  : 'Step size of sell price table',
	CommandLineKeys.BELLS      : 'Total amount of bells used to buy turnips'
}

class Parameters:
	def __init__(self, *args, **kargs):
		self.paras = kargs 
		self.get_paras_from_args(*args)

	def get_paras_from_args(self, *args):
		for key_value in args:
			key, value = self.get_key_value(key_value)
			if not key in self.paras:
				self.paras[key] = value

	def get_key_value(self, key_value):
		key, value = key_value.split('=')
		return (key.strip(), value.strip())

	def try_get(self, key, default):
		if key in self.paras:
			return self.paras[key]
		return default

def round_up(value):
	int_value = int(value)
	if value > float(int_value):
		return int_value + 1
	return int_value

class TurnipWeek:
	def __init__(self, buy_price, sell_price, stacks, cost, profit):
		self.buy_price = buy_price
		self.sell_price = sell_price
		self.stacks = stacks
		self.turnips = self.stacks * Const.TURNIP_INVENTORY_STACK
		self.cost = cost 
		self.profit = profit

	def __str__(self):
		ret_str  = 'Buy: {0} -> Sell: {1}'.format(self.buy_price, self.sell_price)
		ret_str += ' -> Stacks: {0:,} -> Turnips: {1:,}'.format(self.stacks, self.turnips) 
		ret_str += ' -> Cost: {0:,} -> Sold: {1:,}'.format(self.cost, self.get_sold())
		ret_str += '-> Profit: {0:,}'.format(self.profit)
		return ret_str

	def get_profit(buy_price, sell_price, turnips):
		return turnips * (sell_price - buy_price)

	def get_cost(buy_price, turnips):
		return turnips * buy_price

	def get_sold(self):
		return self.turnips * self.sell_price

	def get_week_lacking_profit(buy_price, sell_price, stacks):
		turnips = stacks * Const.TURNIP_INVENTORY_STACK
		cost = TurnipWeek.get_cost(buy_price, turnips)
		profit = TurnipWeek.get_profit(buy_price, sell_price, turnips)
		return TurnipWeek(buy_price, sell_price, stacks, cost, profit)

	def get_week_lacking_sell_price(buy_price, stacks, profit):
		turnips = stacks * Const.TURNIP_INVENTORY_STACK
		sell_price = round_up(profit / turnips + buy_price)
		cost = TurnipWeek.get_cost(buy_price, turnips)
		return TurnipWeek(buy_price, sell_price, stacks, cost, profit)

	def get_week_lacking_turnips(buy_price, sell_price, profit):
		divisor = sell_price - buy_price
		if not divisor == 0:
			turnips = round_up(profit / divisor)
			stacks = turnips // Const.TURNIP_INVENTORY_STACK
			cost = TurnipWeek.get_cost(buy_price, turnips)
			return TurnipWeek(buy_price, sell_price, stacks, cost, profit)
		return None

	def get_week_lacking_loss(buy_price, sell_price, stacks):
		turnips = stacks * Const.TURNIP_INVENTORY_STACK
		cost = TurnipWeek.get_cost(buy_price, turnips)
		loss = turnips * (buy_price - sell_price)
		return TurnipWeek(buy_price, sell_price, stacks, cost, -loss)

class StalkMarket:
	def __init__(self, step_size=10):
		self.turnip_weeks = []
		self.sell_price_gen = (x for x in range(Const.TURNIP_PROFIT_START, Const.TURNIP_HIGH_PRICE + 10, step_size))

	def forecast_profit(self, buy_price, sell_price, stacks):
		turnip_week = TurnipWeek.get_week_lacking_profit(buy_price, sell_price, stacks)
		self.turnip_weeks.append(turnip_week)
		return turnip_week

	def forecast_sell_price(self, buy_price, stacks, profit):
		turnip_week = TurnipWeek.get_week_lacking_sell_price(buy_price, stacks, profit)
		self.turnip_weeks.append(turnip_week)
		return turnip_week

	def forecast_turnip_count(self, buy_price, sell_price, profit):
		turnip_week = TurnipWeek.get_week_lacking_turnips(buy_price, sell_price, profit)
		if not turnip_week == None:
			self.turnip_weeks.append(turnip_week)
		return turnip_week

	def forecast_table(self, buy_price, profit):
		week_table = []
		for price in self.sell_price_gen:
			turnip_week = TurnipWeek.get_week_lacking_turnips(buy_price, price, profit)
			self.turnip_weeks.append(turnip_week)
			week_table.append(turnip_week)
		return week_table

	def forecast_turnip_loss(self, buy_price, sell_price, stacks):
		turnip_week = TurnipWeek.get_week_lacking_loss(buy_price, sell_price, stacks)
		self.turnip_weeks.append(turnip_week)
		return turnip_week

	def get_turnips_from_bells(self, buy_price, amount):
		turnips = round_up(amount / buy_price)
		return (round_up(turnips / Const.TURNIP_INVENTORY_STACK), turnips)

	def divine_sell_price(self):
		pass

class CommandLine:
	def __init__(self, *args, **kargs):
		self.paras = Parameters(*args, **kargs)
		self.task_type = self.paras.try_get(CommandLineKeys.TASK, None)
		self.amount = int(self.paras.try_get(CommandLineKeys.BELLS, 0))
		self.profit = int(self.paras.try_get(CommandLineKeys.PROFIT, 0))
		self.buy_price = int(self.paras.try_get(CommandLineKeys.BUY_PRICE, 0))
		self.sell_price = int(self.paras.try_get(CommandLineKeys.SELL_PRICE, 0))
		self.stacks = int(self.paras.try_get(CommandLineKeys.STACKS, 0))
		self.stalk_market = StalkMarket()

	def print_header(self):
		print()
		print('-' * 40)
		print('- Calulating Stalk Market...')
		print('-' * 40)

	def print_task(self, task_type, message):
		print('{0}={1} -> {2}'.format(CommandLineKeys.TASK, task_type, message))
		print()

	def print_paras(self, para_list):
		print('  - ({0})'.format(', '.join(['{0}= {1}'.format(key, parameter_help[key]) for key in para_list])))
		print()

	def print_help(self):
		print()
		print('Task Type Key: {0}:'.format(CommandLineKeys.TASK))
		print()
		self.print_task(TaskType.TURNIP_HELP, 'Turnip help task')
		self.print_task(TaskType.TURNIP_COUNT, 'Get turnip count needed for given profit')
		self.print_paras([CommandLineKeys.BUY_PRICE, CommandLineKeys.SELL_PRICE, CommandLineKeys.PROFIT])
		self.print_task(TaskType.TURNIP_SELL_PRICE, 'Get sell price for given profit')
		self.print_paras([CommandLineKeys.BUY_PRICE, CommandLineKeys.STACKS, CommandLineKeys.PROFIT])
		self.print_task(TaskType.TURNIP_BOUGHT, 'Get number of turnips bought for given bell amount')
		self.print_paras([CommandLineKeys.BUY_PRICE, CommandLineKeys.BELLS])
		self.print_task(TaskType.TURNIP_PROFIT, 'Get profit for given number of turnips, buy price, and sell price')
		self.print_paras([CommandLineKeys.BUY_PRICE, CommandLineKeys.SELL_PRICE, CommandLineKeys.STACKS])
		self.print_task(TaskType.TURNIP_TABLE, 'Creates a table of weeks with varying sell prices')
		self.print_paras([CommandLineKeys.BUY_PRICE, CommandLineKeys.PROFIT])
		self.print_task(TaskType.TURNIP_LOSS, 'Computes the loss from selling at a lower price than bought')
		self.print_paras([CommandLineKeys.BUY_PRICE, CommandLineKeys.SELL_PRICE, CommandLineKeys.STACKS])

	def ExecuteTask(self):
		if self.task_type == TaskType.TURNIP_HELP:
			self.print_help()
		elif self.task_type == TaskType.TURNIP_COUNT:
			if not self.buy_price == 0 and not self.sell_price == 0 and not self.profit == 0 :
				print(self.stalk_market.forecast_turnip_count(self.buy_price, self.sell_price, self.profit))
		elif self.task_type == TaskType.TURNIP_SELL_PRICE:
			if not self.stacks == 0 and not self.buy_price == 0 and not self.profit == 0:
				print(self.stalk_market.forecast_sell_price(self.buy_price, self.stacks, self.profit))
		elif self.task_type == TaskType.TURNIP_BOUGHT:
			if not self.buy_price == 0 and not self.amount == 0:
				stacks, itemized_turnips = self.stalk_market.get_turnips_from_bells(self.buy_price, self.amount)
				turnips = stacks * Const.TURNIP_INVENTORY_STACK
				out_str = 'Bells: {0:,} -> Buy: {1:,} -> Stacks {2:,} -> Turnips {3:,}'.format(self.amount, self.buy_price, stacks, turnips)
				out_str += ' -> Itemized Turnips: {0:,}'.format(itemized_turnips)
				print(out_str)
		elif self.task_type == TaskType.TURNIP_PROFIT:
			if not self.buy_price == 0 and not self.sell_price == 0 and not self.stacks == 0:
				print(self.stalk_market.forecast_profit(self.buy_price, self.sell_price, self.stacks))
		elif self.task_type == TaskType.TURNIP_TABLE:
			if not self.buy_price == 0 and not self.profit == 0:
				print('\n'.join([str(week) for week in self.stalk_market.forecast_table(self.buy_price, self.profit)]))
		elif self.task_type == TaskType.TURNIP_LOSS:
			if not self.buy_price == 0 and not self.sell_price == 0 and not self.stacks == 0:
				print(self.stalk_market.forecast_turnip_loss(self.buy_price, self.sell_price, self.stacks))

	def run(self):
		if not self.task_type == None:
			self.print_header()
			print()
			self.ExecuteTask()
			print()

if __name__=='__main__':
	import sys 

	command_line = CommandLine(*sys.argv[1:])
	command_line.run()
