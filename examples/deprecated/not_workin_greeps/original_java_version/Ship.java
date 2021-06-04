import greenfoot.*;  // (World, Actor, GreenfootImage, and Greenfoot)
 
/**
 * A space ship. It comes from space, lands, and releases some Greeps into the world.
 * 
 * @author Michael Kolling
 * @version 1.0
 */
public class Ship extends Actor
{
    
    private int totalPassengers = 20;     // Total number of passengers in this ship.
    private int passengersReleased = 0;   // Number of passengers that left so far.
    private Counter foodCounter;          // Tomato counter 
    private int targetPosition;           // The vertical position for landing
    private Timer timer = null;
    private int stepCount = 0;
    
    /**
     * Create a space ship. The parameter specifies at what height to land.
     */
    public Ship(int position)
    {
        targetPosition = position;
    }

    /**
     * Let the ship act: move or release greeps.
     */
    public void act()
    {
        if(inPosition()) {
            if(! isEmpty()) {
                releasePassenger();
            }
        }
        else {
            move();
        }
    }
    
    /**
     * True if all passengers are out.
     */
    public boolean isEmpty()
    {
        return passengersReleased == totalPassengers;
    }
    
    /**
     * Move the ship down (for movement before landing).
     */
    public void move()
    {
        int dist = Math.min((targetPosition - getY()) / 8, 8) + 1;
        setLocation(getX(), getY() + dist);
    }
    
    /**
     * True if we have reached the intended landing position.
     */
    private boolean inPosition()
    {
        return getY() >= targetPosition;
    }
    
    /**
     * Possibly: Let one of the passengers out. Passengers appear at intervals, 
     * so this may or may not release the passenger.
     */
    private void releasePassenger()
    {
        if(passengersReleased < totalPassengers) {
            stepCount++;
            if(stepCount == 10) {
                getWorld().addObject(new Greep(this), getX(), getY() + 30);
                passengersReleased++;
                if(timer == null) {
                    startTimer();
                }
                stepCount = 0;
            }
        }
    }

    /**
     * Record that we have collected another tomato.
     */
    public void storeTomato(Creature cr)
    {
        if(cr.removeTomato() == false) 
            return; // did not have a tomato
            
        if(foodCounter == null) {
            foodCounter = new Counter("Tomatoes: ");
            int x = getX();
            int y = getY() + getImage().getHeight() / 2 + 10;
            if(y >= getWorld().getHeight()) {
                y = getWorld().getHeight();    
            }

            getWorld().addObject(foodCounter, x, y);
        }        
        foodCounter.increment();
    }
    
    /**
     * Return the current count of tomatos collected.
     */
    public int getTomatoCount()
    {
        if(foodCounter == null)
            return 0;
        else
            return foodCounter.getValue();
    }
    
    /**
     * Start the timer that counts time elapsed.
     */
    private void startTimer()
    {
        if(timer == null) {
            timer = new Timer();
            getWorld().addObject(timer, 700, 570);
        }
    }
}