n = 0;
Time  = [];
Voltage = [];
while n < Relaxationperiod(2) -Relaxationperiod(1)
Time(n+1,1) = n;
Voltage(n+1,1) = SearchedVoltage(Relaxationperiod(1)+n);
n=n+1;
end
