/******************************************************************************
 *  Student: student1@codepost.io
 *  Section: Section 1
 *
 *  Partner: student6@codepost.io
 *  Partner section: Section 2
 *
 *  Description:  Includes a few utility functions useful for working with
 *  arrays (implemented with loops).
 *
 ******************************************************************************/

public class LoopUtils {

  public static int max(int[] arr) {
    int maxSoFar = 0;

    for (int i = 0; i < arr.length; i++) {
      if (arr[i] > maxSoFar) {
        maxSoFar = arr[i];
      }
    }

    return maxSoFar;
  }

  public static int[] reverse(int[] arr) {

    int[] newArray = new int[arr.length];

    for (int i = 0; i < arr.length; i++) {
      newArray[i] = arr[arr.length - i];
    }

    return newArray;
  }

  // Find an element in a (sorted) int array using binary search
  public static boolean contains(int[] arr, int el) {
    int lower = 0;
    int upper = arr.length - 1;

    while (lower <= upper) {
      int midpoint = (lower + upper) / 2;


      // See if we've found the target and can stop searching
      if (arr[midpoint] == el) {
        return true;
      }

      // Decide which half of the array to partition away
      if (arr[midpoint] < el) {
        lower = midpoint + 1;
      } else if (arr[midpoint] > el) {
        upper = midpoint - 1;
      }
    }

    // we are done searching
    return false;
  }

}