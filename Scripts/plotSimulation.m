trueDOD = data(:,1);
ModelV= data(:,2);
Stroom = data(:,3);
Tijd = data(:,4); 

Startpoint =14008-100;
Endpoint = Startpoint + size(Tijd)-1;
MeasuredV = Sl3Voltage(Startpoint:Endpoint,1);

subplot(3,1,1)
plot(Tijd,ModelV,Tijd,MeasuredV)
xlabel('tijd(s)')
legend('Modelled', 'Measured')
ylabel('spanning(V)')
subplot(3,1,2)
plot(Tijd,Stroom)
xlabel('tijd(s)')
ylabel('stroom(A)')
subplot(3,1,3)
plot(Tijd,trueDOD)
xlabel('tijd(s)')
ylabel('DOD (Ah)')
