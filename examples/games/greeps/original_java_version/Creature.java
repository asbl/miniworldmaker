import greenfoot.*;  // (World, Actor, GreenfootImage, and Greenfoot)
import java.util.List;

/**
 * A Creature is the base class for all alien beings in this scenario. It
 * provides the basic abilities of creatures in this world.
 * 
 * @author Michael Kolling
 * @version 1.0
 */
public abstract class Creature extends Actor
{
    private static final double WALKING_SPEED = 5.0;
    private static final int TIME_TO_SPIT = 10;

    /** Indicate whether we have a tomato with us */
    private boolean carryingTomato = false;
    
    /** The creature's home ship */
    private Ship ship;

    private boolean moved = false;
    private boolean atWater = false;
    private int timeToSpit = 0;
    
    /** General purpose memory */
    private int memory;
    private boolean[] flags;
    
    /**
     * Create a creature at its ship.
     */
    public Creature(Ship ship)
    {
        this.ship = ship;
        flags = new boolean[2];
        setRotation(Greenfoot.getRandomNumber(360));
    }
    
    
    /**
     * Act - must be called as part of subclass act. This ensures single
     * movement in each act round.
     */
    public void act()
    {
        moved = false;
    }
    
    
    /**
     * Turn 'angle' degrees towards the right (clockwise).
     */
    public void turn(int angle)
    {
        setRotation(getRotation() + angle);
    }
    

    /**
     * Turn in the direction facing the home ship.
     */
    public void turnHome()
    {
        int deltaX = ship.getX() - getX();
        int deltaY = ship.getY() - getY();
        setRotation((int) (180 * Math.atan2(deltaY, deltaX) / Math.PI));
    }
    
    
    /**
     * True if we are at our space ship.
     */
    public final boolean atShip()
    {
         Actor ship = getOneIntersectingObject(Ship.class);
         return ship != null;
    }

    /**
     * Move forward roughly in the current direction. Sometimes we get a 
     * little off course.
     */
    public void move()
    {
        if(moved)   // can move only once per 'act' round
            return;
            
        // there's a 3% chance that we randomly turn a little off course
        if (randomChance(3)) {
            turn((Greenfoot.getRandomNumber(3) - 1) * 10);
        }

        double angle = Math.toRadians( getRotation() );
        int x = (int) Math.round(getX() + Math.cos(angle) * WALKING_SPEED);
        int y = (int) Math.round(getY() + Math.sin(angle) * WALKING_SPEED);
        
        // now make sure that we are not stepping out of the world
        if(x >= getWorld().getWidth()) {
            x = getWorld().getWidth() - 1;
        }
        if(x < 0) {
            x = 0;
        }
        if(y >= getWorld().getHeight()) {
            y = getWorld().getHeight() - 1;
        }
        if(y < 0) {
            y = 0;
        }
        
        if(((Earth)getWorld()).isWater(x, y)) {
            atWater = true;
        }
        else {
            atWater = false;
            setLocation(x, y);
        }
        
        if(timeToSpit > 0)
            timeToSpit--;
            
        moved = true;
    }

    /**
     * To avoid confusion/cheating, calling the built-in Greenfoot
     * move(int amount) does the same as the Creature move() function.
     */
    public void move(int amount)
    {
        move();
    }
    
    
    /**
     * Return true if we have just seen water in front of us.
     */
    public boolean atWater()
    {
        return atWater;
    }
    
    
    /**
     * Load a tomato onto *another* creature. This works only if there is another creature
     * and a tomato pile present, otherwise this method does nothing.
     */
    public final void loadTomato()
    {
        // check whether there's a tomato pile here
        TomatoPile tomatoes = (TomatoPile) getOneIntersectingObject(TomatoPile.class);
        // check whether there's another creature here
        Creature greep = (Creature) getOneIntersectingObject(Creature.class);

        if(greep != null && tomatoes != null) {
            if(!greep.carryingTomato()) {
                tomatoes.takeOne();
                greep.carryTomato();
            }
        }
    }

    
    /**
     * Check whether we can see paint of a given color where we are sitting.
     */
    public boolean seePaint(String color)
    {
        List paintDrops = getIntersectingObjects(Paint.class);
        for(Object obj : paintDrops) {
            if ( ((Paint)obj).getColor().equals(color)) {
                return true;
            }
        }
        return false;
    }

        
    /**
     * Check whether we are carrying a tomato.
     */
    public final boolean carryingTomato()
    {
        return carryingTomato;
    }
        
    /**
     * Remove the tomato currently carried (and return true). Return
     * false if we were not carrying one.
     */
    public final boolean removeTomato()
    {
        if (carryingTomato) {
            carryingTomato = false;
            return true;
        }
        else
            return false;
    }
    

    /**
     * Receive a tomato and carry it.
     */
    private void carryTomato()
    {
        carryingTomato = true;
        setImage(getCurrentImage());
    }

    
    /**
     * Drop the tomato we are carrying. If we are at the ship, it is counted.
     * If not, it's just gone...
     */
    protected final void dropTomato()
    {
        if(!carryingTomato)
            return;
            
        if(atShip()) {
            ship.storeTomato(this);
        }
        carryingTomato = false;
        setImage(getCurrentImage());
    }

    
    /**
     * This method must be defined in subclasses. It gives subclasses the chance
     * to specify their own images.
     */
    abstract public String getCurrentImage();

    
    /**
     * Test if we are close to one of the edges of the world. Return true if we are.
     */
    public boolean atWorldEdge()
    {
        if(getX() < 3 || getX() > getWorld().getWidth() - 3)
            return true;
        if(getY() < 3 || getY() > getWorld().getHeight() - 3)
            return true;
        else
            return false;
    }

    
    /**
     * Return 'true' in exactly 'percent' number of calls. That is: a call
     * randomChance(25) has a 25% chance to return true.
     */
    protected boolean randomChance(int percent)
    {
        return Greenfoot.getRandomNumber(100) < percent;
    }
    
    
    /**
     * Spit a drop of paint onto the ground. We can spit in three colors: "red", "orange",
     * and "purple". (All other strings will be mapped to one of these.)
     */
    public void spit(String color)
    {
        if(timeToSpit == 0) {
            Paint paint = new Paint(color);
            getWorld().addObject(paint, getX(), getY());
            timeToSpit = TIME_TO_SPIT + Greenfoot.getRandomNumber(10);
        }
    }
    
    
    /**
     * Store a user defined value. Attention: even though the parameter type is int,
     * only byte size values (0 <= val <= 255) are accepted.
     */
    public void setMemory(int val)
    {
        if(val < 0 || val > 255)
            throw new IllegalArgumentException("memory value must be in range [0..255]");
        else 
            memory = val;
    }
    
    
    /**
     * Retrieve a previously stored value.
     */
    public int getMemory()
    {
        return memory;
    }


    /**
     * Store a user defined boolean value (a "flag"). Two flags are available, 
     * i.e. 'flagNo' may be 1 or 2.
     */
    public void setFlag(int flagNo, boolean val)
    {
        if(flagNo < 1 || flagNo > 2)
            throw new IllegalArgumentException("flag number must be either 1 or 2");
        else 
            flags[flagNo-1] = val;
    }
    
    
    /**
     * Retrieve the value of a flag. 'flagNo' can be 1 or 2.
     */
    public boolean getFlag(int flagNo)
    {
        if(flagNo < 1 || flagNo > 2)
            throw new IllegalArgumentException("flag number must be either 1 or 2");
        else 
            return flags[flagNo-1];
    }
}
