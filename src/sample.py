
from __future__ import print_function
from mailmerge import MailMerge
from datetime import date

template = "draft-spousal-consent.docx"



people = [
    {
        "spouse_name": "Stuart",
        "spouse_address": "Bristol",
        "borrowers_lawyer": "James"
    },
    {
        "spouse_name": "Kizito",
        "spouse_address": "Kawempe",
        "borrowers_lawyer": "Bosco"
    },
    {
        "spouse_name": "Sanyu",
        "spouse_address": "Wandegeya",
        "borrowers_lawyer": "Ssebagala"
    },
    {
        "spouse_name": "Richard",
        "spouse_address": "Ntinda",
        "borrowers_lawyer": "Antoinette"
    },
]

print('...Generating contracts')
for ob in people:
    document = MailMerge(template)
    document.merge(
        spouse_name = ob["spouse_name"],
        spouse_address = ob["spouse_address"],
        borrowers_lawyer = ob["borrowers_lawyer"]
        )

    document.write(f'contract-{ob["spouse_name"]}.docx')