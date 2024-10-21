public class Main {
    boolean binarySearch(int[] array, int target, int l, int r) {
        if (l > r) return -1;
        int h = (l+r)/2;
        if (array[h] == target) return true;
        if (target < array[h]) return binarySearch(array, target, l, h-1);
        if (target > array[h]) return binarySearch(array, target, h+1, r);

        return false;  // this line doesn't matter, just to have something to return
    }
    // Returns the lowest index where you could insert an element in an array
    int lowerIndex(int[] array, int target, int l, int r) {
        if (l > r) return l;
        int h = (l+r)/2;
        if (target == array[h]) return ...;
        if (target < array[h]) return ...;
        if (target > array[h]) return ...;
        return false;  // doesn't matter again
    }
    // Returns the highest index where you could insert an element in an array
    int upperIndex(int[] array, int target, int l, int r) {
        if (l > r) return l;
        int h = (l+r)/2;
        if (target == array[h]) return ...;
        if (target < array[h]) return ...;
        if (target > array[h]) return ...;
        return false;  // doesn't matter again
    }
}