How-To Guide For Messaging
==========================
In order to follow along with this guide, you will need QUARTET-UI- the user
interface for QU4RTET systems and (optionally) *Docker*.
If you do not have this, you can get it via
the *SerialLab* gitlab page.  If you do not have *Docker* installed, you
can find it here:

https://www.docker.com/


Define An EndPoint
------------------
*EndPoints* define other systems where you'd like to send messages.  The first
thing you'll need to do is define one.  If you'd like to follow along this
guide without a real system to send messages to, you can get an echo HTTP
server here and run it in docker:

https://hub.docker.com/r/mendhak/http-https-echo/

For example, we will define an endpoint to our local echo server as such:

* Name: Local Echo Server
* URN: http://localhost

As you can imagine, this could be any URN value to any external system.
Defining the transport protocol is part of the URN structure...more on that
later.  For now, we will stick with HTTP.

Define Authentication Information
---------------------------------
Let's assume you have to send a message to a trading partner, well they will
most likely be supplying you with a username and a password to use to both
authenticate your system to theirs and to authorize it to send data as well.
The *AuthenticationInfo* database model class in this module handles the
definition of authentication data for communicating with external systems.

For the sake of example, even though the server does not require it, we will
set up an Authentication Information record with the following attributes:

* username: TestUser
* password: TestPassword
* type: Digest
* description: A test user for our example.

Define An EPCIS Output Criteria Record
--------------------------------------
The *EPCISOutputCriteria* database model allows one to define a series of
attributes that one might expect to see in certain EPCIS events that should
trigger the sending of a message to a trading partner system, for example.
For this example walk-through, let's configure a criteria record that looks
for EPCIS Transaction Events that are of Action ADD and have a bizLocation
of *urn:epc:id:sgln:305555.123456.0*:

* Name: Test Transaction Criteria
* Action: ADD
* Event Type: Transaction
* Business Location: urn:epc:id:sgln:305555.123456.0

We could even fine tune this criteria record more by adding other event
attributes but we will keep it simple for the sake of example.

Set Up A Criteria Rule
----------------------
So now, we've told the system the following things:

# *what to look for*
# *where to send data*
# *how to identify itself to other systems*

Our next step will be to use the `quartet_capture` rule engine framework to
consume inbound messages, parse them and apply the filter criteria we have
already set up.

To get started, set up a new
rule with the following attributes (use QUARTET-UI to do this):

* Name: EPCIS Output Filter
* Description: Examines inbound data for output criteria.

Set Up The Criteria / Filtering Step
++++++++++++++++++++++++++++++++++++
The first *Step* in our *Rule* will be one that, while parsing EPCIS events,
looks through each event for the criteria we set up in our *EPCISOutputCriteria*
record.  Configure a step with the following attributes:

* Step: Inspect EPCIS
* Description: Parse and insepect EPCIS events using output criteria.
* Class Path: quartet_output.steps.OutputParsingStep
* Execution Order: 1

Tell The Filter Step To Use Our Critieria
+++++++++++++++++++++++++++++++++++++++++
The filtering step we set up above needs to know that we want it to use
our *Test Transaction Criteria*  that we defined at the beginning of this
exercise.  We can do this by adding a *Step Parameter* to the Step.  Go ahead
and add a *Step Parameter* with the following values:

Name:

Set Up a Commissioning Data Step (Optional)
+++++++++++++++++++++++++++++++++++++++++++
Let's say, for example, we've filtered out a Transaction Event that has
5 epcs within it and we'd like to have the commissioning events for those
5 epcs and all of their children in an outbound message.  To accomplish this,
we can add a commissioning data step.

Create a step with the following configuration attributes:

* Step: Add Commissioning Data
* Description: Adds commissioning events for filtered EPCs and their children.
* Class Path: epcis_output.steps.AddCommissioningDataStep
* Execution Order: 2

Set Up an Aggregation Data Step (Optional)
++++++++++++++++++++++++++++++++++++++++++
Let's say that we'd also like to include any aggregation events for any
EPCs found in the filtered message- all the way down the packaging hierarchy
of each. For example, if there were a pallet EPC in a filtered event, we'd
want all of the aggregation information for

* Step: Add Aggregation Data
* Description: Adds aggregation events for included EPCs in any filtered events.
* Class Path: quartet_output.steps.UnpackHierarchyStep
* Execution Order: 3

Quick Review
++++++++++++
So far we have done the following:

# Instructed the system to "look" for Transaction Events of type ADD coming
  from a specific business location.
# Told the system to gather all of the commissioning data for any EPCs
  (and children) within any events that meet the criteria above.
# Told the system to also add Aggregation events for any EPCs that were found
  in any of the Transaction Events from step 1.

In the first step, we're filtering events out as they come into the system.
The first step will take any events that meet our criteria and pass them
downstream to any steps after.  The second step will create new object
events (commissioning events) and pass them downstream as well.  The third
step will do something simililar by creating aggregation data for any EPCs
found in the first filtered message.

Set Up A Step That Renders a Message
++++++++++++++++++++++++++++++++++++
So the first three steps filter data and then send it "down" the rule to
further steps.  The Aggregation and Commissioning steps both pass EPCPyYes
EPCIS event classes down to subsequent steps.  So what we will do now is
add a step that looks for any `EPCPyYes` events (for more on EPCPyYes see
https://gitlab.com/serial-lab/EPCPyYes) and then *renders* those events to
EPCIS compliant XML.

In QUARTET-UI, set up a step with the following:

* Step: Render EPCIS XML
* Description: Pulls any EPCPyYes objects from the context and creates an XML message.
* Class Path: quartet_output.steps.EPCPyYesOutputStep
* Execution Order: 4

This step, again, will find any events that have been created by the prior two
steps and render them to XML (along with the first filtered Transaction
event as well).

Create A Task That Creates An Outbound Task- Wait, what?
++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Once we've rendered a messsage we need to, obviously, send it somewhere.
Having said that, we most likely don't want to send the message directly
inside of this Rule since, if it were to fail during the transport phase,
we'd have to roll back all of the EPCIS data stored in the database and
destroy the created message- even though it was simply a network failure.
It's probably better to put the message on a queue and let the system try
(and retry) sending it in a separate Rule/Task alltogether.  **So that's
what we'll do!**

Create a step with the following:

* Step: Queue Outbound Message
* Description: Creates a Task in the rule engine for sending any outbound data.
* Class Path: quartet_output.steps.CreateOutputTaskStep
* Order: 5


Set Up A Transport Rule
-----------------------
