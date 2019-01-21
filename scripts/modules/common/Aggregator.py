Aggregator = {}

function Aggregator:new(aggr_per)
	newObj = {
		aggr_per = aggr_per,
		next_period_is_found = false,
		m15 = {'0000', '0015', '0030', '0045', '0100', '0115', '0130', '0145', '0200', '0215', '0230', '0245', '0300', '0315', '0330', '0345', '0400', '0415', '0430', '0445', '0500', '0515', '0530', '0545', '0600', '0615', '0630', '0645', '0700', '0715', '0730', '0745', '0800', '0815', '0830', '0845', '0900', '0915', '0930', '0945', '1000', '1015', '1030', '1045', '1100', '1115', '1130', '1145', '1200', '1215', '1230', '1245', '1300', '1315', '1330', '1345', '1400', '1415', '1430', '1445', '1500', '1515', '1530', '1545', '1600', '1615', '1630', '1645', '1700', '1715', '1730', '1745', '1800', '1815', '1830', '1845', '1900', '1915', '1930', '1945', '2000', '2015', '2030', '2045', '2100', '2115', '2130', '2145', '2200', '2215', '2230', '2245', '2300', '2315', '2330', '2345'},
		m30 = {'0000', '0030', '0100', '0130', '0200', '0230', '0300', '0330', '0400', '0430', '0500', '0530', '0600', '0630', '0700', '0730', '0800', '0830', '0900', '0930', '1000', '1030', '1100', '1130', '1200', '1230', '1300', '1330', '1400', '1430', '1500', '1530', '1600', '1630', '1700', '1730', '1800', '1830', '1900', '1930', '2000', '2030', '2100', '2130', '2200', '2230', '2300', '2330'},
		m60 = {'0000', '0100', '0200', '0300', '0400', '0500', '0600', '0700', '0800', '0900', '1000', '1100', '1200', '1300', '1400', '1500', '1600', '1700', '1800', '1900', '2000', '2100', '2200', '2300'},
		OHLC_agg = {},
		last_agg_time = nil,
		last_r_cnt = 1,
		next_period_is_found,
		started = false
	}
	self.__index = self
	return setmetatable(newObj, self)
end

function Aggregator:find_next_period(o,h,l,c, t)
	if self.aggr_per == 15 then
		aggr_time_range = self.m15
	elseif self.aggr_per == 30 then
		aggr_time_range = self.m30
	elseif self.aggr_per == 60 then
		aggr_time_range = self.m60
	else
		return nil
	end
	
	hours = string.sub(t, 1, 2)
	minutes = string.sub(t, 3, 4)
	cmp = hours .. minutes
	
	r_cnt = self.last_r_cnt
	while  r_cnt <= #aggr_time_range and cmp >= aggr_time_range[r_cnt] do
		r_cnt = r_cnt + 1
	end
	if r_cnt > #aggr_time_range then
		r_cnt = 1
	end
	
	agg_time = aggr_time_range[r_cnt]
	if self.last_agg_time ~= nil then
		if self.last_agg_time ~= aggr_time_range[r_cnt] then
			self.last_agg_time = aggr_time_range[r_cnt]
			self.last_r_cnt = r_cnt
			return true
		end
	else
		self.last_agg_time = aggr_time_range[r_cnt]
		self.last_r_cnt = r_cnt
		return true
	end
	self.last_agg_time = aggr_time_range[r_cnt]
	return false
end

function Aggregator:aggregate(o,h,l,c,t)
	self.next_period_is_found = self:find_next_period(o,h,l,c,t)
	if self.next_period_is_found ~= nil then
		if self.next_period_is_found then
			if self.started then
				-- prev aggr_per is completed
				return self.OHLC_agg
			end
			-- next aggr_per is started
			self.OHLC_agg['O'] = o
			self.OHLC_agg['H'] = h
			self.OHLC_agg['L'] = l
			self.OHLC_agg['C'] = c
			self.OHLC_agg['T'] = t
			self.started = true
		else
			-- aggregate data
			self.OHLC_agg['H'] = math.max(self.OHLC_agg['H'], h)
			self.OHLC_agg['L'] = math.min(self.OHLC_agg['L'], l)
			self.OHLC_agg['C'] = c
			self.OHLC_agg['T'] = t
		end
	end
	return {}
end