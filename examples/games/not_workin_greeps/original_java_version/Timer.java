import greenfoot.*;  // (World, Actor, GreenfootImage, and Greenfoot)

/**
 * A timer is a conter that automatically counts up as time goes on.
 * This timer also checks whether the map has been completed (either time
 * is up, or all tomatoes are gone).
 * 
 * @author M Kolling
 * @version 1.0
 */
public class Timer extends Counter
{
    private static final int GAME_TIME = 120;
    
    private int tick;
    
    public Timer()
    {
        super("Time: ");
        tick = 0;
    }
    
    /**
     * Count time. Notify of 'Game Over' when game time is reached.
     */
    public void act() 
    {
        tick++;
        if(tick == 10) {
            increment();
            tick = 0;
            checkFinish();
        }
    }
    
    /**
     * Check whether this map is finished. This is the case if time is up, or 
     * all tomatoes are gone.
     */
    private void checkFinish()
    {
        if(timeOut() || allTomatoesGone()) {
            gameOver();
        }
    }
    
    /**
     * Return true if game time is up.
     */
    private boolean timeOut()
    {
        return getValue() >= GAME_TIME;
    }
    
    /**
     * Return true if there are no tomatoes left in this map.
     */
    private boolean allTomatoesGone()
    {
        return getWorld().getObjects(TomatoPile.class).isEmpty();
    }
    
    /**
     * Notify that the level is over.
     */
    private void gameOver()
    {
        ((Earth)getWorld()).mapFinished(GAME_TIME - getValue());
    }
}
