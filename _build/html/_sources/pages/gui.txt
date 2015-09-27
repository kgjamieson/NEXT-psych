.. include:: links.rst

============================
Web user interface
============================

Launching the web interface
---------------------------
*This assumes you have your Amazon AWS keys and credintials. If not or any
errors are encountered, visit* :ref:`setup`.

.. code-block:: shell

    export AWS_ACCESS_KEY_ID=<access>
    export AWS_SECRET_ACCESS_KEY=<secret>
    export KEY_FILE=/Users/scott/Classes/security/AWS/SS_NEXT.pem
    export KEY_PAIR=SS_NEXT
    alias next_ec2='python next_ec2.py --key-pair=$KEY_PAIR --identity-file=$KEY_FILE'

    python next_ec2.py --key-pair=$KEY_PAIR --identity-file=$KEY_FILE launch <clustername>

Then visit the URL ``http://<ec2-public-dns>`` and the web interface is there!
The ``<ec2-public-dns>`` can be found on Amazon's AWS EC2 dashboard and
selecting your instance.

.. image:: imgs/ec2-public-dns.png

.. note:: This process of launching an instance. In a separate terminal, you can run ``next_ec2 stop <clustername>`` to stop EC2 billing and the instance and ``next_ec2 start <clustername> to restart it. This is a quicker than terminating the instance via ``next_ec2 terminate <instancename>``

.. todo:: Make a GUI to run this script. I'd like to have double-click to launch NEXT... or have the user log into their Amazon account and *that's it*. That should be fairly easy with Amazon's AWS SDK.

Data formatting
---------------
Two files are needed:

* a zip file. This zip file should contain images/etc.
* a CSV file. This CSV file should have 3 rows. The first row should be the
  filename, the second should the filetype (image, video) and the third should
  be an alternate description. No header should be included in this CSV file!
  An example CSV file is shown below

.. code-block:: python

   01F_AN_O.jpeg,image,01F_AN_O.jpeg
   01F_CA_C.jpeg,image,01F_CA_C.jpeg
   01F_CA_O.jpeg,image,01F_CA_O.jpeg
   01F_DI_C.jpeg,image,01F_DI_C.jpeg


.. warning:: A header should not be included in this CSV file!
.. todo:: Actually check the second column of the CSV file. I know image works but I am not sure what else works
.. todo:: Verify videos/animations work.
.. todo:: See where the alternate description shows up. Maybe it's only in the dataset and never visible by the user?

Launching a new experiment
--------------------------

Replicating an experiment
-------------------------
.. todo:: How to include your own data?

Viewing the results
-------------------
Go to URL ``http://<ec2-public-dns>:8000/dashboard/experiment_list``. This will
provide a lot of graphs and rankings for all your experiments.

.. todo:: No link from NEXT GUI to the NEXT backend is available. See `NEXT-psych issue #2`_

.. _`NEXT-psych issue #2`: https://github.com/kgjamieson/NEXT-psych/issues/2
