from datetime import date

from flask import abort, Blueprint, g, flash
from flask import redirect, render_template, request
from flask import url_for

from blog.auth.views import login_required
from blog.pages.model import Page
from blog.pages.model import PageElement

bp = Blueprint('pages', __name__)


def get_page(path):
    page = Page.query.filter_by(path_name=path).first()

    if page is None:
        abort(404, "Page id {} not found".format(id))

    return page


@bp.route('/<string:path>', methods=('GET',))
def page_view(path):

    from blog.pages.model import PageElement
    page = get_page(path)
    pages = Page.query.all()
    # name = page.path_name

    page_sections = PageElement.query.filter_by(
        parent=page.path_name).order_by(PageElement.created_at.asc()).all()

    # Placement for POST directive to create page elements

    return render_template('blog/page.html',
                           page=page, pages=pages, page_sections=page_sections)


"""
    This section hold the methods for creating,
    updating and deleting elements or sections on pages.
    These elements are stored in the database as PageElement classes
"""


@bp.route('/create_elem', methods=('GET', 'POST'))
@login_required
def elem_new():
    """
        Create a new PageElement class on a Page class
    """
    if request.method == 'POST':
        title = request.form['header']
        body = request.form['body']
        parent = request.args.get('parent')
        error = None

        if not title:
            error = "You need to give this page element a header."

        if error is not None:
            flash(error)
        else:
            from blog import db
            elem = PageElement(title=title, body=body,
                               author_id=g.user.uid, parent=parent)
            db.session.add(elem)
            db.session.commit()

            return page_view(elem.parent)

    return render_template('/page/new_elem.html')


@bp.route('/section/update', methods=('GET', 'POST'))
@login_required
def elem_update():
    section_id = request.args.get('section')
    page_section = PageElement.query.get(section_id)

    if request.method == 'POST':
        title = request.form['header']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            from blog import db
            page_section.title = title
            page_section.body = body
            db.session.commit()
            return page_view(page_section.parent)

    return render_template('page/elem_update.html', elem=page_section)


@bp.route('/section/<int:id>/delete', methods=('POST',))
@login_required
def elem_delete(id):
    from blog import db
    page_section = PageElement.query.get(id)
    db.session.delete(page_section)
    db.session.commit()
    return page_view(page_section.parent)


"""END SECTION"""


@bp.route('/new_page', methods=('GET', 'POST'))
@login_required
def page_new():
    # now = datetime.now()
    # day = now.strftime("%d")
    # month = now.strftime("%m")

    if request.method == 'POST':
        path_name = request.form['path_name']
        page_name = request.form['page_name']
        error = None

        if not path_name:
            error = "You need to give this page a name, "
            error += "no spaces or special characters allowed.\n"
            error += "Underscores, numbers and '%' are permitted."
        if error is not None:
            flash(error)
        else:
            from blog import db
            page = Page(path_name=path_name, page_name=page_name,
                        author_id=g.user.uid)
            db.session.add(page)
            db.session.commit()

            return page_view(path_name)

    return render_template('/page/new_page.html')


@bp.route('/<string:path>/delete', methods=('GET',))
@login_required
def page_del(path):

    from blog import db
    page = Page.query.filter_by(path_name=path).first()
    db.session.delete(page)
    db.session.commit()
    return redirect('/')
