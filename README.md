This package facilitates using **docassemble** for document assembly
from Legal Server.

It creates a new API endpoint at `/newlssession` that accepts a
POST. The endpoint creates a new session in an interview and
pre-populates variables in the session based on the data fields passed
to the endpoint. It accepts a special data field `yaml`, which must
contain the filename of an interview on your system. This package
contains a test interview,
`docassemble.lsdocumentassembly:data/questions/test.yml` that you can
use as a guide.

The suggested way to use this with Legal Server is to take advantage
of the Guided Navigation feature of Legal Server, which has an
advanced feature called "Perform an API call." You can create a Guided
Navigation dialogue that calls the **docassemble** API and populates a
custom field in the case called "URL for document assembly" with a URL
that when clicked will take the user to a **docassemble** interview
where variables have been pre-populated with values from the Legal
Server case.

# Docassemble setup

On your **docassemble** server, log in as an administrator and go to
Profile, API keys. Create an API key and write it down somewhere. You
will need it later.

Go to Package Management and set the GitHub URL to the URL of this
repository, which is
`https://github.com/jhpyle/docassemble-lsdocumentassembly`. Then press
"Update" to install this package.

Create an interview on your server similar to the [`test.yml`]
interview that is provided with this package. The main things to note
are:

1. There is a `code` block with `mandatory: True` that sets
   `multi_user = True`. This is important.
2. The `objects` block is modified with `mandatory: True`. This is
   important if you need to pre-populate variables that are attributes
   of objects; an attribute cannot be pre-populated unless the
   underlying object instance already exists. The `mandatory: True` on
   the `objects` block ensures that the objects are created when the
   session starts.

# Legal Server setup

Go to Admin, Custom Field Management and do Actions -> Create a New
Custom Field. Select the Module "Case," Class Name "matter," Type
"text," and set the Short Name to "URL for document assembly" or some
other name of your choosing.

Go to Admin, Guided Navigation and click the "Create interactive
dialogue" button. Set the Dialogue name to "Retainer agreement" or
whatever you want to give as a name for your interview process. The
user will see this name on the screen.

Click "Add new segment." Call your segment "First segment" or some
other name of your choosing (only administrators will see it).

Click "Add element" and set the Element type to "Action: Perform an
API call."

Set the URL of the API call to
`https://your.docassemble.server/newlssession`, substituting the
actual name of your **docassemble** server in place of
`your.docassemble.server`.

Set the Method to "POST."

Set the Post type to "JSON."

Set the HTTP Headers to:

    X-API-Key: t0Ll8QGmXO5ctZ4H0UipFrBuGfhwGqS2

but instead of `t0Ll8QGmXO5ctZ4H0UipFrBuGfhwGqS2` put in the API key
you obtained earlier.

Set Authentication to "No authentication." The API endpoint actually
does have authentication, but it uses the HTTP headers for
authentication instead of "HTTP basic authentication" or "Bearer
token."

Check the checkbox next to "Perform request asynchronously."

Under Parameters, click "Add parameter" and add a parameter of type
"Static parameter." Set the "Parameter key" to "yaml" and the "Static
value" to the interview filename of the interview on your
**docassemble** server that you wish to launch. You can

You can add additional parameters of type "Value from a field" in
order to pre-set variables in your **docassemble** interview. Put the
variable name in "Parameter key" and select the Legal Server field
under "Choose field." Do not check "Path parameter."

The sample interview uses the following variables and fields:

* `client.name.first` for the "First Name" of the client.
* `client.name.last` for the "Last Name" of the client.
* `ls_id` for the "Matter/Case ID#" of the case.

Below the Parameters, check the checkbox next to "Update Case from
response." Click "Add field to set" and choose the "URL for document
assembly" field that you created earlier. Set "Jq Filter" to `.url`
and don't forget to include the period at the beginning, because it is
very important.

Click "Add element" to add a second element to the Segment. Set the
Element type to "Field to capture" and set "Field to populate" to "URL
for document assembly."

Set the Label to "URL."

Check the checkbox next to "Field should be read-only."

Under "Default destination," select "Exit this dialogue."

Click "Save segment."

Click "Save dialogue."

Under Admin, "Processes, Forms, and Profiles," do Actions -> New
Auxiliary Form.

Give the form a Name like "Retainer agreement" to match the Guided
Navigation dialogue you created earlier.

Select the "Yes" button next to "Create New Process Containing This
Form?"

Set "Active" to "Yes."

Set "Add Continue Button" to "Yes.

Under "Form Elements," select Block from the dropdown menu. Select the
"Dialogue Runner" block. Click "Add."

Under "Dialogue to run," select the Dialogue you just created.

Next, under "Form Elements," set the dropdown to Instruction and click
"Add." Open the Instruction and check the "Format as HTML"
checkbox. Fill in the Text of the instruction with the following:

    <div id="dialogueinst"></div>
    <script>
      document.getElementById("dialogueinst").parentNode.style.display="none";
      for(var rows = document.querySelectorAll('.rrow > span'), i = rows.length; i--;){
        if (rows[i].innerHTML && rows[i].innerHTML.match(/^https?:.*/)){
             rows[i].innerHTML = "<a href=\"" + rows[i].innerHTML + "\" target=\"_blank\">" + rows[i].innerHTML + "<\/a>";
        }
      }
    </script>

Adding this instruction is not necessary; all it does is make the "URL
for document assembly" clickable.

Under Admin, "Processes, Forms, and Profiles," go to the Menu Boxes
tab and edit the menu boxes for your main case profile. Under
"Side/Action Elements," edit your "Custom Link Box Actions" and add a
menu item for the "process" called "Retainer agreement."

To test this, go to a case and select "Retainer agreement" from the
actions menu. If all goes well, the "URL for document assembly" will
be populated with a URL when the page appears.

[`test.yml`]: https://github.com/jhpyle/docassemble-lsdocumentassembly/blob/main/docassemble/lsdocumentassembly/data/questions/test.yml
