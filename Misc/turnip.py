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
	TURNIP_STALK_LINES = 'tsl'
	TURNIP_PROFIT      = 'tp'

class CommandLineKeys:
	TASK       = '-tk'
	BUY_PRICE  = '-bp'
	SELL_PRICE = '-sp'
	PROFIT     = '-p'
	STACKS     = '-s'
	TURNIPS    = '-t'
	STEP_SIZE  = '-ss'
	BELLS      = '-bll'

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
	return int(value) + 1

class Turnips:
	def __init__(self, *args, **kargs):
		self.paras = Parameters(*args, **kargs)
		self.stacks = self.paras.try_get(CommandLineKeys.STACKS, 0)
		self.turnips = self.paras.try_get(CommandLineKeys.TURNIPS, 0)
		self.buy_price = self.paras.try_get(CommandLineKeys.BUY_PRICE, 0)
		self.sell_price = self.paras.try_get(CommandLineKeys.SELL_PRICE, 0)
		self.profit = self.paras.try_get(CommandLineKeys.PROFIT, 0)

	def __str__(self):
		ret_str  = 'Buy: {0} -> Sell: {1}'.format(self.buy_price, self.sell_price)
		ret_str += ' -> Stacks {0:,} -> Turnips: {1:,}'.format(self.stacks, self.turnips) 
		ret_str += ' -> Cost: {2:,} -> Profit: {5:,}'.format(self.get_cost(), self.profit)
		return ret_str

	def get_cost(self):
		return self.buy_price * self.turnips

	def turnip_count(self):
		if not self.buy_price == 0 and not self.sell_price == 0 and not self.profit == 0:
			self.stacks = self.get_turnip_stack_number(self.sell_price)
			self.turnips = self.stacks * Const.TURNIP_INVENTORY_STACK
			return self
		return None

	def turnip_sell_price(self):
		if not self.buy_price == 0 and not self.turnips == 0 and not self.profit == 0:
			self.sell_price = self.get_turnip_sell_price()
			return self
		return None

	def turnips_bought(self, money):
		if not self.buy_price == 0:
			self.turnips = self.get_turnips_bought(money)
			self.stacks = self.turnips // Const.TURNIP_INVENTORY_STACK
			return self
		return None

	def turnip_profit(self):
		if not self.buy_price == 0 and not self.sell_price == 0 and not self.turnips == 0:
			self.profit = self.get_turnip_profit()
			return self
		return None

	def get_turnip_stack_number(self, sell_price):
		return round_up(self.profit / (100*(self.sell_price - self.buy_price)))

	def get_turnip_sell_price(self):
		return round_up((self.profit / self.turnips) + self.buy_price)

	def get_turnips_bought(self, money):
		return money // self.buy_price

	def get_turnip_profit(self):
		return self.turnips * (self.sell_price - self.buy_price)

class CommandLine:
	def __init__(self, *args, **kargs):
		self.paras = Parameters(*args, **kargs)
		self.task_type = self.paras.try_get(CommandLineKeys.TASK, None)
		self.sell_step = self.paras.try_get(CommandLineKeys.STEP_SIZE, 10)
		self.money = self.paras.try_get(CommandLineKeys.BELLS, 0)
		self.turnips = Turnips(*args, **kargs)
		self.sell_gen = (x for x in range(Const.TURNIP_PROFIT_START, Const.TURNIP_HIGH_PRICE + 10, self.sell_step))

	def print_header(self):
		print('-' * 40)
		print('- Calulating Stalk Market...')
		print('-' * 40)

	def print_task(self, task_type, message):
		print('{0} = {1} -> {2}'.format(CommandLineKeys.TASK, task_type, message))

	def print_command_key(self, key, message):
		print('{0} -> {1}'.format(key, message))

	def print_help(self):
		print()
		print('Task Type Key: {0}:'.format(CommandLineKeys.TASK))
		self.print_task(TaskType.TURNIP_HELP, 'Turnip help task')
		self.print_task(TaskType.TURNIP_COUNT, 'Get turnip count needed for given profit')
		self.print_task(TaskType.TURNIP_SELL_PRICE, 'Get sell price for given profit')
		self.print_task(TaskType.TURNIP_BOUGHT, 'Get number of turnips bought for given bell amount')
		self.print_task(TaskType.TURNIP_STALK_LINES, 'Graph lines of turnips needed for given sell price and profit')
		self.print_task(TaskType.TURNIP_PROFIT, 'Get profit for given number of turnips, buy price, and sell price')
		print()
		print('Turnip Command Line Parameters:')
		self.print_command_key(CommandLineKeys.BUY_PRICE, 'Sunday turnip price')
		self.print_command_key(CommandLineKeys.SELL_PRICE, 'Nook buy price')
		self.print_command_key(CommandLineKeys.PROFIT, 'Turnip profit')
		self.print_command_key(CommandLineKeys.STACKS, 'Stacks of 100 turnips')
		self.print_command_key(CommandLineKeys.TURNIPS, 'Number of turnips')
		self.print_command_key(CommandLineKeys.STEP_SIZE, 'Graph step size for each turnip sell price')
		self.print_command_key(CommandLineKeys.BELLS, 'Bells spent on turnips')
		print()

	def ExecuteTask(self):
		if self.task_type == TaskType.TURNIP_HELP:
			self.print_help()
		elif self.task_type == TaskType.TURNIP_COUNT:
			turnip_count = self.turnips.turnip_count()
			if not turnip_count == None:
				print(turnip_count)
		elif self.task_type == TaskType.TURNIP_SELL_PRICE:
			turnip_sell_price = self.turnips.turnip_sell_price()
			if not turnip_sell_price == None:
				print(turnip_sell_price)
		elif self.task_type == TaskType.TURNIP_BOUGHT:
			turnips_bought = self.turnips.turnips_bought(self.money)
			if not turnips_bought == None:
				print(turnips_bought)
		elif self.task_type == TaskType.TURNIP_PROFIT:
			turnip_profit = self.turnips.turnip_profit()
			if not turnip_profit == None:
				print(turnip_profit)
		elif self.task_type == TaskType.TURNIP_STALK_LINES:
			for price in self.sell_gen:
				self.turnips.sell_price = price
				turnip_count = self.turnips.turnip_count()
				if not turnip_count == None:
					print(turnip_count)

	def run(self):
		if not self.task_type == None:
			self.print_header()
			self.ExecuteTask()

if __name__=='__main__':
	import sys 

	command_line = CommandLine(*sys.argv[1:])
	command_line.run()
