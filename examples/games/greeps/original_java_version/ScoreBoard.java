import greenfoot.*;  // (World, Actor, GreenfootImage, and Greenfoot)
import java.awt.Color;
import java.awt.Font;
import java.util.Calendar;

/**
 * The ScoreBoard is used to display results on the screen. It can display some
 * text and several numbers.
 * 
 * @author M Kolling
 * @version 1.0
 */
public class ScoreBoard extends Actor
{
    public static final float FONT_SIZE = 48.0f;
    public static final int WIDTH = 600;
    public static final int HEIGHT = 400;
    
    public ScoreBoard()
    {
        makeImage("Scores", "Score: ", "nobody", 100);
    }

    /**
     * Create a score board for an interim result.
     */
    public ScoreBoard(String title, String text, String prefix, int map, int[] scores)
    {
        makeImage(title, text, prefix, scores[map]);
        addMapScores(map, scores);
    }
    
    /**
     * Create a score board for the final result.
     */
    public ScoreBoard(String title, String text, String prefix, int[] scores)
    {
        int total = 0;
        for(int val : scores) {
            total += val;
        }
        makeImage(title, text, prefix, total);
        addMapScores(scores.length-1, scores);
        printResultToTerminal(title, scores);
    }
    
    /**
     * Make the score board image.
     */
    private void makeImage(String title, String text, String prefix, int score)
    {
        GreenfootImage image = new GreenfootImage(WIDTH, HEIGHT);

        image.setColor(new Color(0, 0, 0, 128));
        image.fillRect(0, 0, WIDTH, HEIGHT);
        image.setColor(new Color(0, 0, 0, 128));
        image.fillRect(5, 5, WIDTH-10, HEIGHT-10);
        Font font = image.getFont();
        font = font.deriveFont(FONT_SIZE);
        image.setFont(font);
        image.setColor(Color.WHITE);
        image.drawString(title, 60, 100);
        image.drawString(text, 60, 220);
        image.drawString(prefix + score, 60, 320);
        setImage(image);
    }
    
    /**
     * Add the scores for the individual maps to the score board. 'scores' is an
     * array with all scores, 'mapNo' is the number of the current map (array entries
     * past this value have no valid value).
     */
    private void addMapScores(int mapNo, int[] scores)
    {
        GreenfootImage image = getImage();
        Font font = image.getFont();
        font = font.deriveFont(20.0f);
        image.setFont(font);
        image.setColor(Color.WHITE);
        for(int i = 0; i <= mapNo; i++) {
            image.drawString("Map " + (i+1) + ": " + scores[i], 460, 80+(i*28));
        }
    }
    
    private void printResultToTerminal(String name, int[] scores)
    {
        Calendar now = Calendar.getInstance();
        String time = now.get(Calendar.HOUR_OF_DAY) + ":";
        int min = now.get(Calendar.MINUTE);
        if(min < 10)
            time += "0" + min;
        else
            time += min;
        System.out.print(time + ":  [");
        int total = 0;
        for(int score : scores) {
            total += score;
            if (score < 10)
                System.out.print("  " + score);
            else
                System.out.print(" " + score);
        }
        System.out.println("]  " + total + "  -- " + name );
    }
}
