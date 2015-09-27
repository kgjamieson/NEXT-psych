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

Launching a new experiment
--------------------------
.. todo:: How to launch a new experiment?

Replicating an experiment
-------------------------
.. todo:: How to include your own data?
