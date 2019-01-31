SMA = {}

function SMA:new(avg_per)
	newObj = {
		avg_per = avg_per or 1,
		rolling_sum = 0,
		buffer = Buffer:new(avg_per),
		last_mode = nil
	}
	self.__index = self
	return setmetatable(newObj, self)
end

function SMA:calc(new_item)
	if self.last_mode == 'u' then
		self.rolling_sum = self.rolling_sum + new_item - self.buffer.buff[1] + self.buffer.buff[self.buffer.size]
	else 
		self.rolling_sum = self.rolling_sum + new_item
	end
	
	self.buffer:slide(new_item)
	self.last_mode = 'c'
	if self.buffer.is_ready then
		local sma_val = self.rolling_sum / self.avg_per
		self.rolling_sum = self.rolling_sum - self.buffer.buff[1]
		return sma_val
	end
end

function SMA:update(new_item)
	if self.last_mode == 'c' then
		self.rolling_sum = self.rolling_sum + new_item + self.buffer.buff[1] - self.buffer.buff[self.buffer.size]
	else 
		self.rolling_sum = self.rolling_sum + new_item
	end
	
	self.buffer:update(new_item)
	self.last_mode = 'u'
	if self.buffer.is_ready then
		local sma_val = self.rolling_sum / self.avg_per
		self.rolling_sum = self.rolling_sum - new_item
		return sma_val
	end
end