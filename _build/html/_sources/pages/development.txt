.. _development:

=================
Development
=================

.. todo:: Include development tips (and ask Lalit!)

Workflow
--------

Personally, I have four terminal windows open. One to do each of the following
tasks:

.. image:: imgs/development_flow.png

1. Run ``next_ec2 launch cluster_name``
2. One to run ``next_ec2 rsync``. This will propogate the changes I make
   locally.
3. One to run ``docker-compose {stop, up}``. These commands require to be logged
   into the docker instance via ``next_ec2 docker_login cluster_name``. This
   stops and starts the servers after making a change.
4. One to run ``docker-compute logs`` to view debugging output.

