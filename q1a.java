/*

Scoring guidelines:
https://apcentral.collegeboard.org/media/pdf/ap23-sg-computer-science-a.pdf

*/

(a)
public int findFreeBlock(int period, int duration) {
    int free = -1;
    for (int i = 0; i < 60 - duration + 1; i++) {
        int count =0 ;
        for (int j = i; j < i+duration; j++) {
            if (isMinuteFree(period, j)) {
                count++;
            }
            if (count == duration) {
                free = i;
            }
        }
    }
    return free;
}

(b)
public boolean makeAppointment(int startPeriod, int endPeriod, int duration) {
    int s = 0;
    for (int p = startPeriod; p < endPeriod+1; p++) {
        if (findFreeBlock(p, duration) != -1) {
            s = findFreeBlock(p, duration);
            reserveBlock(p, s, duration);
            return true;
        } else {
            return false;
        }
    }
}
