Compute Scaling factors
-----------------------

1- In the `Tools` menu, select `SF Calculator`.
A new window will pop-up.

2- The new window only has one activated field to enter a range of run
numbers. Enter the following run range: `184975-184989` and click enter.

3- The table will be populated with all the runs in the selected range.
For each run, the peak will be selected automatically. You can browse through the runs
to verify that the selection was good.

4- Using the browse button, you can select the location of the output file
that will be generated.

5- The `manual` and `sort` buttons are advanced features only used by instrument
scientists. We will leave off of this basic use-case.

6- Clicking the `Generate Scaling Factors` button will perform the
calculation and write the file. The file in `docs/data/sf-test.cfg` contains
the output the run range above should produce.

7- Clicking the `Export script` will allow you to export a Mantid script
that will produce the same result.
