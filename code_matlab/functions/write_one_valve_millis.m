function write_one_valve_millis(ser, valv, millis)
    % ser: serialport objesi
    % valv: int, 0-1-2 veya 1-2-3 (Arduino ile uyumlu olmalı)
    % millis: ms cinsinden (+ inflate, - deflate)

    if millis > 0
        cmd = sprintf('f,%d,%d\n', valv, round(millis)); % inflate
    else
        cmd = sprintf('e,%d,%d\n', valv, round(abs(millis))); % deflate
    end

    pause(0.01); % Komutun iletilmesi için bekleme (Python kodunda da var)
    writeline(ser, cmd); % veya fprintf(ser, cmd); eski serial için
end
