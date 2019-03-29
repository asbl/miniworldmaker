import greenfoot.*;  // (World, Actor, GreenfootImage, and Greenfoot)

import java.awt.Color;
import java.awt.Graphics;
import java.awt.image.BufferedImage;

/**
 * Paint drops that can be left on the ground. Unfortunately, the ground is soft, and 
 * paint sinks in with time. After some time, it will have disappeared.
 * 
 * @author Michael Kolling
 * @version 1.0.1
 */
public class Paint extends Actor
{
    private final static int MAX_INTENSITY = 255;
    private final static int SIZE = 20;
    private int intensity;
    private String name;
    private int red, green, blue;


    /**
     * Create some paint, of default color.
     */
    public Paint()
    {
        this("");
    }
    
    /**
     * Create some paint, of specific fixed colors. Legal color values are:
     * "red", "orange", and "purple".
     */
    public Paint(String color)
    {
        name = color;
        if(color.equals("red")) {
            red = 232; green = 21; blue = 27;
        }
        else if(color.equals("orange")) {
            red = 245; green = 131; blue = 14;
        }
        else {
            name = "purple";
            red = 115; green = 74; blue = 153;
        }
        intensity = MAX_INTENSITY;
        GreenfootImage image = new GreenfootImage(SIZE + 1, SIZE + 1);
        setImage(image);
        updateImage();
    }

    /**
     * With passing time, the color fades, and will eventually disappear.
     */
    public void act()
    {
        intensity -= 1;
        if (intensity <= 0) {
            getWorld().removeObject(this);
        }
        else {
            if ((intensity % 4) == 0) {
                updateImage();
            }
        }
    }

    /**
     * Return the color name of this paint drop.
     */
    public String getColor()
    {
        return name;
    }
    
    /**
     * Make the image
     */
    private void updateImage()
    {
        GreenfootImage image = getImage();
        image.clear();
        int alpha = intensity / 2;
        image.setColor(new Color(red, green, blue, alpha));
        image.fillOval(0, 0, SIZE, SIZE);
    }
}
