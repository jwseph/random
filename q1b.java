(a)
public int findFreeBlock(int period, int duration) {
    boolean open;
    for (int i = 0; i <= 59; i++) {
        if (isMinuteFree(period, i)) {
            open = true;
            return i;
        } else {
            open = false;
            return i;
        }
    }
}

(b)
public boolean makeAppointment(int startPeriod, int endPeriod, int duration) {
    for (int i = startPeriod; i <= endPeriod; i++) {
        if (isMinuteFree(i, findFreeBlock(i, duration)) {
            reserveBlock(i, findFreeBlock(i, duration), duration);
            return true;
        } else {
            return false;
        }
    }
}