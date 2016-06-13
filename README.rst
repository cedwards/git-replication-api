git-replication-api
===================

This repository contains a SaltStack state file, it's configuration and scripts. The state was originally written on FreeBSD, so it may require some tweaking (primarily just paths) to work elsewhere. The hope is, if you understand Salt states, that you'll understand how this works--it should be somewhat self explanatory.

What does this do?
------------------

This is my first attempt at building an API-based service. In this case it is a service to replicate source code from GitHub (or an internal GitHub enterprise) into internal development or production environments. In this particular case there are three distinct environments in the design:

.. code-block:: yaml

    corp -> dmz -> prod

This API is designed to replicate source code by way of an http(s) endpoint. Specific endpoints trigger different actions, such as a `git fetch` vs a `git clone` or a `git init`.

The API then reads a `replication.map` of your environment where you can define which systems should notify which other systems, and there really shouldn't be any limit to the depth of your map. In this case, again, it is just corp, dmz and prod, but the map is designed to be flexible enough to layer over whatever network topology you have.

