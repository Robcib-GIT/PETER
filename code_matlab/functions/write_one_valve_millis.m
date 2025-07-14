function write_one_valve_millis(ser, valv, millis)
    % ser: serialport object
    % valv:  1-2-3-4-5-6
    % millis: ms(+ inflate, - deflate)

    if millis > 0
        cmd = sprintf('f,%d,%d\n', valv, round(millis)); % inflate
    else
        cmd = sprintf('e,%d,%d\n', valv, round(abs(millis))); % deflate
    end

    pause(0.01); 
    writeline(ser, cmd); 
end
