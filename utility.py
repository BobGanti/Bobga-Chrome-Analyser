


class Month:

    def month_value(self, mm):
        val = 0
        if mm == 'Jan':
            val = '01'
        elif mm == 'Feb':
            val = '02'
        elif mm == 'Mar':
            val = '03'
        elif mm == 'Apr':
            val = '04'
        elif mm == 'May':
            val = '05'
        elif mm == 'Jun':
            val = '06'
        elif mm == 'Jul':
            val = '07'
        elif mm == 'Aug':
            val = '08'
        elif mm == 'Sep':
            val = '09'
        elif mm == 'Oct':
            val = '10'
        elif mm == 'Nov':
            val = '11'
        elif mm == 'Dec':
            val = '12'
        else:
            val = '0'

        return val
