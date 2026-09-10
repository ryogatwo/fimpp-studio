package regression;
public class Fixture {
    public int count = 3;
    public static int TOTAL = 7;
    private boolean ready;
    public Fixture() {}
    public Fixture(int count) { this.count = count; }
    public void setCount(int value) { count = value; }
    public int getCount() { return count; }
    public void setReady(boolean value) { ready = value; }
    public boolean isReady() { return ready; }
    public int getPlus(int value) { return count + value; }
    public static int twice(int value) { return value * 2; }
}
