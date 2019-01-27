Buffer = {}

function Buffer:new(size)
	newObj = {
		size = size or 1,
		buff = {},
		is_ready = false
	}
	self.__index = self
	return setmetatable(newObj, self)
end

function Buffer:slide(new_item)
	if #self.buff < self.size then
		table.insert(self.buff, new_item)
		if #self.buff == self.size then
			self.is_ready = true
		end
	else
		table.remove(self.buff, 1)
		table.insert(self.buff, new_item)
	end
end

function Buffer:update(new_item)
	if #self.buff == self.size then
		self.buff[self.size] = new_item
	end
end
