

from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.libs import helpers, assertions

from .schema import AssignmentSchema, AssignmentSubmitSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    """Returns list of assignments"""
    teachers_assignments = Assignment.get_assignments_by_teachers(p.teacher_id)
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)

@teacher_assignments_resources.route('/assignments/grade', methods=['GET','POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignments(p, incoming_payload):
    """Grades assignment assigned to a teacher"""   
    _id = incoming_payload["id"]
    _grade = incoming_payload["grade"]

    graded_assignment = Assignment.grade_submitted_assignments(_id, _grade, principal=p)
        
    db.session.commit()

    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
  
    return APIResponse.respond(data=graded_assignment_dump)

































